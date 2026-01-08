# `Image Utilities`

Batch tools for processing NFT images without altering visual quality.

## Included Tools

### `resize_pngs.py`
- Scales PNG images to 50% of original dimensions
- Preserves transparency
- Outputs to `resized/`

### `png_to_webp.py`
- Converts PNG images to **lossless WebP**
- Keeps original filenames
- Outputs to `webp/`

### `resize_webp.py`
- Resizes WebP images to **512 x 512**
- Lossless output
- Outputs to `resized_webp/`

## Usage

Run any tool from the folder containing your NFT images:

```bash
python C:/Users/<your user>/nft-asset-generator/image/<script>.py
