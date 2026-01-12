import json
import os
from pathlib import Path
import subprocess
import sys


def test_duplicate_traits_are_detected(tmp_path):
    """
    Creates two metadata files with identical trait combinations.
    The validator should FAIL.
    """

    metadata_dir = tmp_path / "metadata"
    metadata_dir.mkdir()

    meta_1 = {
        "tokenId": 1,
        "attributes": [
            {"trait_type": "Background", "value": "Gold"},
            {"trait_type": "Body", "value": "Blue"},
        ],
    }

    meta_2 = {
        "tokenId": 2,
        "attributes": [
            {"trait_type": "Background", "value": "Gold"},
            {"trait_type": "Body", "value": "Blue"},
        ],
    }

    (metadata_dir / "1.json").write_text(json.dumps(meta_1), encoding="utf-8")
    (metadata_dir / "2.json").write_text(json.dumps(meta_2), encoding="utf-8")

    repo_root = Path(__file__).resolve().parents[1]
    validator = repo_root / "metadata" / "validate_supply.py"

    # Force UTF-8 for the child process I/O on Windows
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"

    result = subprocess.run(
        [sys.executable, str(validator)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )

    assert result.returncode != 0

    stdout = result.stdout or ""
    stderr = result.stderr or ""
    combined = (stdout + "\n" + stderr).lower()

    # Be flexible: your script may say "duplicate", "uniqueness", etc.
    assert ("duplicate" in combined) or ("unique" in combined) or ("uniqueness" in combined)
