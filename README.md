# NFT Asset Generator (ERC-721 Compatible)

A configurable Python-based asset generation pipeline for creating ERC-721 NFT collections.  
This tool combines layered image assets using weighted rarity rules and outputs both images and Ethereum-compatible metadata.

---

## Features

- Layered asset composition using ordered image stacks
- Weighted rarity system for fine-grained trait distribution
- Optional trait inclusion for limited-accessory NFTs
- ERC-721 compatible metadata generation
- Fully configurable asset paths, layers, and rarity weights

---

## Tech Stack

- Python 3
- Pillow (PIL)
- JSON


---

## Usage

Configure asset paths, rarity weights, and layer order in the script, then run:


generate_nfts(
    total_nfts=100,
    accessories_per_nft=5
)
Generated images and metadata will be written to the output/ directory.

Configuration

Asset Paths
Assets are grouped by category and defined in the asset_paths dictionary.
Categories can be added or removed as needed.

Rarity Weights
Trait rarity is controlled via weighted probability lists:

rarity_weights = {
    "background": [50, 50, 50, 50],
    "body": [80, 70, 100],
    "eyes": [2, 90, 50],
    "head": [60, 40, 80],
    "accessory": [95, 2, 2]
}
Higher weights increase the likelihood of selection.

Layer Order
layer_order = [
    "background",
    "body",
    "head",
    "eyes",
    "accessory"
]
Layers are composited from bottom to top.

Output
Each generated NFT includes:

A composite PNG image

A corresponding JSON metadata file compatible with ERC-721 standards

Design Notes

Rarity weights allow precise control of trait distribution

Metadata follows ERC-721 conventions for marketplace compatibility

License
MIT License
