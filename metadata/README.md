# `Metadata Utilities`

A set of lightweight, purpose-built tools for validating and preparing NFT metadata for deployment and marketplace use.

## Included Tools

### `validate_supply.py`
- Automatically verifies matching image (`<id>.png`) and metadata (`<id>.json`) files
- Validates JSON structure
- Checks **trait combination uniqueness** across the collection
- Prints all results directly to the console (no arguments required)

### `trait_report.py`
- Scans all metadata files and prints **trait frequency and percentage** across total supply
- Sorted by most common values per trait
- Console-only analysis (no CSV or arguments needed)

### `update_ipfs_cid.py`
- Batch rewrites the `image` field in all metadata files using a single IPFS CID base
- Preserves `name`, `description`, `external_url`, `attributes`, `tokenId`, and `properties`
- Outputs updated files into `./new_metadata/` (original metadata is left untouched)
- Prompts for CID interactively at runtime (no CLI arguments)

## Usage
Run any tool from the folder containing your NFT images.

### License
MIT
