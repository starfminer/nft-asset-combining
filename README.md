# `NFT Asset Generator (ERC-721 Compatible)`

A configurable Python-based asset generation pipeline for creating ERC-721 NFT collections.

This tool combines layered image assets using weighted rarity rules and outputs both final images and Ethereum-compatible metadata.

 

## Features

- Layered asset composition using ordered image stacks
- Weighted rarity system for fine-grained trait distribution
- Optional rarity inclusion for limited accessories
- ERC-721 compatible metadata generation
- Fully configurable asset paths, layers, and rarity weights


## Tech Stack

- Python 3
- Pillow (PIL)
- JSON


## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/freeman-james/nft-asset-generator.git
cd nft-asset-generator
pip install pillow
```

# Configuration

## Asset Paths

Assets are grouped by category and defined in the asset_paths dictionary:

```bash
asset_paths = {
    "background": [...],
    "body": [...],
    "head": [...],
    "eyes": [...],
    "accessory": [...]
}
```

Categories can be added or removed as needed.

 

## Rarity Weights

Trait rarity is controlled via weighted probability lists:


```bash
rarity_weights = {
    "background": [50, 50, 50, 50],
    "body": [80, 70, 100],
    "eyes": [5, 90, 50],
    "head": [60, 40, 80],
    "accessory": [95, 2, 2]
}
```


Higher weights increase the likelihood of selection.

 

## Layer Order

Layers are composited from bottom to top:

```bash
layer_order = [
    "background",
    "body",
    "head",
    "eyes",
    "accessory"
]
```

Adjust this order to fit your asset design.

 

## Output

Each generated NFT includes:

- A composite PNG image

- A corresponding JSON metadata file compatible with ERC-721 standards


## Usage

Use this script to generate NFT assets and metadata before deployment.

1. Configure your layers: set asset paths, rarity weights, and layer order in the script.

2. Generate metadata:

```bash
generate_metadata_for_all_nfts(100)  # Creates metadata for 100 NFTs
```
Metadata is saved in output/metadata/.

3. Generate images:

```bash
generate_images_from_metadata()  # Generates images from metadata
```

Images are saved directly in output/.



## Design Notes

Weighted rarity allows precise control over trait distribution

Metadata follows ERC-721 conventions for marketplace compatibility

Designed for extensibility and reuse across multiple collections

 

### License

MIT License
