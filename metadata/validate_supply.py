import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path


ID_RE = re.compile(r"^(\d+)\.(png|json)$", re.IGNORECASE)


def collect_ids(folder: Path, exts: tuple[str, ...]) -> dict[int, Path]:
    """
    Collect files named like {id}.{ext} where id is an integer.
    Returns mapping id -> path.
    """
    mapping: dict[int, Path] = {}
    if not folder.exists():
        return mapping

    for p in folder.iterdir():
        if not p.is_file():
            continue
        if p.suffix.lower() not in exts:
            continue

        m = ID_RE.match(p.name)
        if not m:
            continue
        token_id = int(m.group(1))
        mapping[token_id] = p

    return mapping


def find_duplicates(folder: Path) -> list[str]:
    if not folder.exists():
        return []
    names = [p.name.lower() for p in folder.iterdir() if p.is_file()]
    counts = Counter(names)
    return [name for name, c in counts.items() if c > 1]


def try_load_json(path: Path) -> tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8") as f:
            json.load(f)
        return True, ""
    except Exception as e:
        return False, str(e)


def main():
    parser = argparse.ArgumentParser(
        description="Validate NFT supply integrity: matching image+metadata IDs, missing/extra IDs, and JSON validity."
    )
    parser.add_argument("--images-dir", default=".", help="Folder containing PNG files (default: current folder)")
    parser.add_argument("--metadata-dir", default="metadata", help="Folder containing JSON metadata (default: metadata)")
    parser.add_argument("--min-id", type=int, default=None, help="Minimum token ID expected (optional)")
    parser.add_argument("--max-id", type=int, default=None, help="Maximum token ID expected (optional)")
    parser.add_argument(
        "--check-image-field",
        action="store_true",
        help='If set, checks metadata["image"] ends with "<id>.png" (best-effort).',
    )

    args = parser.parse_args()

    images_dir = Path(args.images_dir).resolve()
    metadata_dir = Path(args.metadata_dir).resolve()

    print(f"Images dir:   {images_dir}")
    print(f"Metadata dir: {metadata_dir}")
    print("")

    # Duplicates by name
    img_dupes = find_duplicates(images_dir)
    meta_dupes = find_duplicates(metadata_dir)

    if img_dupes:
        print("⚠️ Duplicate image filenames detected (case-insensitive):")
        for n in img_dupes:
            print(f"  - {n}")
        print("")
    if meta_dupes:
        print("⚠️ Duplicate metadata filenames detected (case-insensitive):")
        for n in meta_dupes:
            print(f"  - {n}")
        print("")

    image_ids = collect_ids(images_dir, (".png",))
    meta_ids = collect_ids(metadata_dir, (".json",))

    if not image_ids:
        print("❌ No PNG files found named like 1.png, 2.png, ... in images dir.")
        sys.exit(1)

    if not meta_ids:
        print("❌ No JSON metadata files found named like 1.json, 2.json, ... in metadata dir.")
        sys.exit(1)

    image_set = set(image_ids.keys())
    meta_set = set(meta_ids.keys())

    missing_images = sorted(meta_set - image_set)
    missing_meta = sorted(image_set - meta_set)
    common = sorted(image_set & meta_set)

    # Determine expected range
    min_id = args.min_id if args.min_id is not None else (min(common) if common else None)
    max_id = args.max_id if args.max_id is not None else (max(common) if common else None)

    if min_id is not None and max_id is not None:
        expected = set(range(min_id, max_id + 1))
        gap_images = sorted(expected - image_set)
        gap_meta = sorted(expected - meta_set)
    else:
        expected = None
        gap_images, gap_meta = [], []

    print("=== Supply Summary ===")
    print(f"Images found:   {len(image_set)}")
    print(f"Metadata found: {len(meta_set)}")
    if common:
        print(f"Overlapping IDs: {len(common)} (min={min(common)}, max={max(common)})")
    print("")

    if missing_images:
        print(f"❌ Missing images for {len(missing_images)} IDs (present in metadata, missing PNG):")
        print("   " + ", ".join(map(str, missing_images[:50])) + (" ..." if len(missing_images) > 50 else ""))
        print("")
    if missing_meta:
        print(f"❌ Missing metadata for {len(missing_meta)} IDs (present in images, missing JSON):")
        print("   " + ", ".join(map(str, missing_meta[:50])) + (" ..." if len(missing_meta) > 50 else ""))
        print("")

    if expected is not None:
        if gap_images:
            print(f"❌ Image ID gaps in expected range {min_id}-{max_id}:")
            print("   " + ", ".join(map(str, gap_images[:80])) + (" ..." if len(gap_images) > 80 else ""))
            print("")
        if gap_meta:
            print(f"❌ Metadata ID gaps in expected range {min_id}-{max_id}:")
            print("   " + ", ".join(map(str, gap_meta[:80])) + (" ..." if len(gap_meta) > 80 else ""))
            print("")

    # JSON validity check
    bad_json = []
    for token_id in common:
        ok, err = try_load_json(meta_ids[token_id])
        if not ok:
            bad_json.append((token_id, err))

    if bad_json:
        print(f"❌ Invalid JSON in {len(bad_json)} metadata files:")
        for token_id, err in bad_json[:10]:
            print(f"  - {token_id}.json: {err}")
        if len(bad_json) > 10:
            print("  ...")
        print("")
    else:
        print("✅ All overlapping metadata files are valid JSON.")
        print("")

    # Optional: check metadata image field ends with "<id>.png"
    if args.check_image_field:
        mismatches = []
        for token_id in common:
            try:
                with meta_ids[token_id].open("r", encoding="utf-8") as f:
                    data = json.load(f)
                img_field = data.get("image", "")
                if not isinstance(img_field, str) or not img_field.lower().endswith(f"/{token_id}.png") and not img_field.lower().endswith(f"{token_id}.png"):
                    mismatches.append((token_id, img_field))
            except Exception as e:
                mismatches.append((token_id, f"(error reading: {e})"))

        if mismatches:
            print(f"⚠️ metadata.image field mismatches for {len(mismatches)} tokens (showing up to 10):")
            for token_id, v in mismatches[:10]:
                print(f"  - {token_id}.json image: {v}")
            if len(mismatches) > 10:
                print("  ...")
            print("")
        else:
            print('✅ metadata["image"] fields look consistent with "<id>.png" (best-effort check).')
            print("")

    # Exit code: fail if critical issues
    critical = bool(missing_images or missing_meta or (expected is not None and (gap_images or gap_meta)) or bad_json)
    if critical:
        print("❌ Validation FAILED (see issues above).")
        sys.exit(2)

    print("✅ Validation PASSED.")
    sys.exit(0)


if __name__ == "__main__":
    main()
