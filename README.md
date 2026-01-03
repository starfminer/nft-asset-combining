NFT Generator Script

This Python script generates unique NFTs by combining various asset layers (e.g., backgrounds, bodies, heads, eyes, accessories) into one image. The script allows for customizable rarity, inclusion of different asset layers, and automatic metadata generation in Ethereum-compatible format (ERC-721 standard).

Features

Asset Layer Combination: Combines multiple layers (background, body, head, eyes, accessories) to generate unique NFTs.

Customizable Rarity: Control the probability of each asset being selected by defining rarity weights for each layer.

Random Accessory Inclusion: Optionally include accessories in a limited number of NFTs by specifying the probability.

Metadata Generation: Generates metadata for each NFT in the Ethereum-compatible ERC-721 format, including attributes like background, body, eyes, accessories, etc.

Flexible Asset Paths: Easily update paths for different asset categories (backgrounds, bodies, eyes, heads, accessories).

Adjustable Weights: Define the weights for asset rarity to control the distribution of different asset types.

Requirements

To run this script, you'll need:

Python 3.x

Pillow (Python Imaging Library) for image manipulation

Install Pillow using pip:

pip install pillow

Usage

Clone the repository:

git clone https://github.com/yourusername/nft-generator.git
cd nft-generator


Prepare Your Assets:
Organize your assets into the following folders:

assets/Background/ — For background images

assets/Body/ — For body images

assets/Eyes/ — For eye images

assets/Head/ — For head images

assets/Accessory/ — For accessory images (optional, can include None for no accessory)

Run the Script:

Edit the script to specify the number of NFTs you want to generate and the number of NFTs that should include accessories.

Example:

generate_nfts(100, accessories_per_nft=5)  # Generate 100 NFTs, with accessories included in 5 NFTs


This will generate the images and metadata in the output/ folder.

Check the Output:

Generated images will be saved in the output/ folder as nft_1.png, nft_2.png, etc.

Metadata files for each NFT will be saved as nft_1.json, nft_2.json, etc., containing image paths and attributes.

Customization
Asset Categories

The assets for each category are defined in the asset_paths dictionary:

background: List of background images (e.g., background1.png, background2.png).

body: List of body images (e.g., body1.png, body2.png).

eyes: List of eye images (e.g., laser.png, lazy.png).

head: List of head images (e.g., beanie.png, visor.png).

accessory: List of accessory images (e.g., bird.png, pipe.png). You can also include None to represent the case when no accessory is added.

Rarity Weights

You can adjust the rarity of each asset layer by modifying the rarity_weights dictionary. For example:

rarity_weights = {
    'background': [50, 50, 50, 50, 50, 50, 50, 50],  # Equal chance for each background
    'body': [80, 70, 70, 100, 60, 90, 80, 50],  # Some body types are rarer
    'eyes': [2, 90, 50],  # One eyes type is very rare
    'head': [60, 50, 100, 40, 80, 70, 90, 50],  # Some heads are rarer
    'accessory': [95, 2, 2]  # 95% chance of choosing None (no accessory)
}


This configuration controls how likely each asset is to be chosen. For instance, accessory: [95, 2, 2] means that there is a 95% chance that no accessory will be chosen, and a 2% chance for each accessory type.

Asset Layer Control

The layer_order list defines the order in which the assets are stacked. By default, the order is:

layer_order = ['background', 'body', 'head', 'eyes', 'accessory']


You can adjust this order or remove layers depending on your requirements.

Adjusting the Number of Accessories

In the generate_nfts function, you can control how many NFTs will have accessories:

generate_nfts(100, accessories_per_nft=5)  # 100 NFTs, 5 with accessories


This will include accessories in 5 out of 100 NFTs. The rest will not have any accessories.

License

This project is licensed under the MIT License - see the LICENSE
 file for details.

Feel free to modify the repository URL in the Clone the repository section and make any other custom adjustments.

Let me know if you'd like additional modifications or have any questions!
