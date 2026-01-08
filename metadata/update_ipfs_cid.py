import json
import re
from pathlib import Path

ID_JSON = re.compile(r"^(\d+)\.json$", re.IGNORECASE)


def normalize_cid_base(s: str) -> str:
    """
    Accepts:
      - examplecid...
      - ipfs://examplecid...
      - ipfs://examplecid.../
      - ipfs://ipfs/examplecid... (normalizes)
    Returns: ipfs://<cid>/  (always ends with /)
    """
    s = s.strip()

    # Common user paste: ipfs://<cid>/...
    if s.startswith("ipfs://"):
        s = s[len("ipfs://") :]

    # If they pasted ipfs://ipfs/<cid> or ipfs://ipfs/<cid>/...
    if s.startswith("ipfs/"):
        s = s[len("ipfs/") :]
    if s.startswith("/"):
        s = s[1:]

    # remove trailing slashes
    s = s.strip("/")

    return f"ipfs://{s}/"


def main():
    cwd = Path(".").resolve()
    meta_dir = cwd / "metadata"
    out_dir = cwd / "new_metadata"
    out_dir.mkdir(exist_ok=True)

    if not meta_dir.exists():
        raise SystemExit(
            "❌ No ./metadata folder found. Run this from the folder that contains the metadata/ directory."
        )

    cid_in = input("Paste IPFS CID base (CID or ipfs://CID/): ").strip()
    if not cid_in:
        raise SystemExit("❌ No CID provided.")

    cid_base = normalize_cid_base(cid_in)
    print(f"Using base: {cid_base}")
    print(f"Writing updated metadata to: {out_dir}")

    updated = 0

    for path in sorted(meta_dir.iterdir(), key=lambda p: p.name):
        if not path.is_file():
            continue
        m = ID_JSON.match(path.name)
        if not m:
            continue

        token_id = m.group(1)  # string

        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        # Build new fields
        filename = f"{token_id}.png"
        new_image = f"{cid_base}{filename}"

        # Apply updates
        data["image"] = new_image

        # Ensure properties.files exists and is correct
        props = data.get("properties")
        if not isinstance(props, dict):
            props = {}
            data["properties"] = props

        files = props.get("files")
        if not isinstance(files, list) or len(files) == 0 or not isinstance(files[0], dict):
            props["files"] = [{"uri": filename, "type": "image/png"}]
        else:
            props["files"][0]["uri"] = filename
            props["files"][0]["type"] = "image/png"

        # Remove asset_paths if present (not needed on-chain / marketplaces)
        data.pop("asset_paths", None)

        # Optional: force symbol (commented out by default)
        # data["symbol"] = "YACHTBOTZ"

        # Write updated JSON to new_metadata/<id>.json (leave originals untouched)
        out_path = out_dir / path.name
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        updated += 1

    print(f"✅ Done. Updated {updated} metadata files into ./new_metadata.")


if __name__ == "__main__":
    main()
