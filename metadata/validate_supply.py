import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

ID_JSON_RE = re.compile(r"^(\d+)\.json$", re.IGNORECASE)
ID_IMG_RE = re.compile(r"^(\d+)\.png$", re.IGNORECASE)


def collect_ids(folder: Path, is_image=False) -> dict[int, Path]:
    mapping = {}
    if not folder.exists():
        return mapping

    for p in folder.iterdir():
        if not p.is_file():
            continue
        if is_image and not p.suffix.lower() == ".png":
            continue
        if not is_image and not p.suffix.lower() == ".json":
            continue

        m = ID_IMG_RE.match(p.name) if is_image else ID_JSON_RE.match(p.name)
        if not m:
            continue
        token_id = int(m.group(1))
        mapping[token_id] = p

    return mapping


def trait_signature(data: dict) -> str:
    """
    Create deterministic signature from attributes to validate uniqueness.
    """
    attrs = data.get("attributes", [])
    if not isinstance(attrs, list):
        return "attributes:INVALID"

    pairs = []
    for a in attrs:
        if not isinstance(a, dict):
            continue
        t = str(a.get("trait_type", "")).strip().lower()
        v = str(a.get("value", "")).strip().lower()
        pairs.append((t, v))

    pairs.sort()
    return "|".join(f"{t}={v}" for t, v in pairs)


def validate_uniqueness(meta_files: dict[int, Path]) -> bool:
    sig_map = {}
    dupes = []

    for token_id, path in meta_files.items():
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"❌ {path.name} invalid JSON: {e}")
            return False

        sig = trait_signature(data)

        if sig in sig_map:
            dupes.append((token_id, sig_map[sig]))
        else:
            sig_map[sig] = token_id

    if dupes:
        print(f"❌ Duplicate trait combinations found: {len(dupes)}")
        for a, b in dupes[:20]:
            print(f"  - Token {a} duplicates token {b}")
        if len(dupes) > 20:
            print("  ...")
        return False

    print("✅ All metadata trait combinations are unique.\n")
    return True


def main():
    images_dir = Path(".").resolve()
    metadata_dir = Path("metadata").resolve()

    print(f"📁 Scanning Images:   {images_dir}")
    print(f"📁 Scanning Metadata: {metadata_dir}\n")

    img_ids = collect_ids(images_dir, is_image=True)
    meta_ids = collect_ids(metadata_dir)

    if not img_ids:
        print("❌ No PNG images found named like 1.png, 2.png, ...")
        sys.exit(1)

    if not meta_ids:
        print("❌ No metadata JSON files found named like 1.json, 2.json, ... in /metadata")
        sys.exit(1)

    img_set = set(img_ids.keys())
    meta_set = set(meta_ids.keys())
    common = sorted(img_set & meta_set)

    print("=== Supply Summary ===")
    print(f"Images found:   {len(img_set)}")
    print(f"Metadata found: {len(meta_set)}")
    print(f"Overlapping IDs: {len(common)}")
    if common:
        print(f"ID range detected: {min(common)} – {max(common)}")
    print("")

    # Validate missing files
    missing_images = sorted(meta_set - img_set)
    missing_meta = sorted(img_set - meta_set)

    if missing_images:
        print(f"❌ Missing images for {len(missing_images)} IDs:")
        print("  " + ", ".join(map(str, missing_images[:50])) + (" ..." if len(missing_images) > 50 else "") + "\n")
    if missing_meta:
        print(f"❌ Missing metadata for {len(missing_meta)} IDs:")
        print("  " + ", ".join(map(str, missing_meta[:50])) + (" ..." if len(missing_meta) > 50 else "") + "\n")

    if missing_images or missing_meta:
        sys.exit(2)

    # Auto-run uniqueness validation if metadata exists
    print("🔍 Validating trait uniqueness...\n")
    if not validate_uniqueness({i: meta_ids[i] for i in common}):
        print("❌ Uniqueness validation failed.")
        sys.exit(3)

    print("✅ All checks passed. Collection is valid and unique.")
    sys.exit(0)


if __name__ == "__main__":
    main()
