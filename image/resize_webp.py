import os
from PIL import Image
from pathlib import Path

OUTPUT_DIR = "resized_webp"
Path(OUTPUT_DIR).mkdir(exist_ok=True)

for filename in os.listdir("."):
    if not filename.lower().endswith(".webp"):
        continue

    with Image.open(filename) as img:
        img = img.convert("RGBA")  # preserve transparency
        img = img.resize((512, 512), Image.LANCZOS)
        out_path = os.path.join(OUTPUT_DIR, filename)
        img.save(out_path, format="WEBP", lossless=True, method=6)

    print(f"✅ Resized: {filename} → {out_path}")

print("✅ Done. Check ./resized_webp")
