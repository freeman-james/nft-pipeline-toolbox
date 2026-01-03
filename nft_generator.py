import random
from PIL import Image
import json
import os

# Define paths to assets
asset_paths = {
    'background': [
        'assets/Background/Aqua.png',
        'assets/Background/Blue.png',
        'assets/Background/Copper.png',
        'assets/Background/Dark Grey.png',
        'assets/Background/Gold.png',
        'assets/Background/Green.png',
        'assets/Background/Light Blue.png',
        'assets/Background/Purple.png'
    ],
    'body': [
        'assets/Body/Blazer.png',
        'assets/Body/Blue Hawaiian.png',
        'assets/Body/Green Hawaiian.png',
        'assets/Body/Normal.png',
        'assets/Body/Pink Button Down.png',
        'assets/Body/Stripes.png',
        'assets/Body/Vest.png',
        'assets/Body/White Polo.png'
    ],
    'eyes': [
        'assets/Eyes/Laser.png',
        'assets/Eyes/Lazy.png',
        'assets/Eyes/Round.png'
    ],
    'head': [
        'assets/Head/Beanie.png',
        'assets/Head/Captains Hat.png',
        'assets/Head/Normal.png',
        'assets/Head/Palm Leaf Hat.png',
        'assets/Head/Slick Hair.png',
        'assets/Head/Straw Hat.png',
        'assets/Head/Visor.png',
        'assets/Head/Wavy Hair.png'
    ],
    'accessory': [
        None,  # no accessory
        'assets/Accessory/Bird.png',
        'assets/Accessory/Pipe.png'
    ]
}

# Define the rarity weights for each category (1 being rare, 100 being common)
rarity_weights = {
    'background': [50, 50, 50, 50, 50, 50, 50, 50],  # All backgrounds equally common
    'body': [50, 50, 50, 50, 50, 50, 50, 50],  # Adjusted body rarity weights
    'eyes': [2, 90, 20],  # Adjusted eyes rarity weights
    'head': [50, 50, 50, 50, 50, 50, 50, 50],  # Adjusted head rarity weights
    'accessory': [90, 5, 5]  # 90% chance of choosing None (no accessory)
}

# Define layer order for merging
layer_order = ['background', 'body', 'head', 'eyes', 'accessory']

# Function to choose an asset based on rarity
def choose_asset(layer):
    weight = rarity_weights[layer]
    chosen_index = random.choices(range(len(asset_paths[layer])), weights=weight, k=1)[0]
    return asset_paths[layer][chosen_index]

# Function to merge assets
def merge_assets(layers):
    # Start with the background layer
    base_image = Image.open(choose_asset('background'))
    
    # Iterate through the layers and add them
    for layer in layers[1:]:
        asset = choose_asset(layer)
        if asset is not None:  # If the chosen asset is not None, merge it
            asset_image = Image.open(asset)
            base_image.paste(asset_image, (0, 0), asset_image) 

    return base_image

# Function to generate metadata for the NFT
def generate_metadata(token_id, image_path, attributes):
    metadata = {
        "name": f"NFT #{token_id}",
        "description": "Generated NFT Collection",
        "external_url": "https://yourwebsite.com",  # Replace with project website
        "image": f"ipfs://your-ipfs-url/{token_id}.png",  # IPFS URL for the image - will be updated later
        "attributes": attributes,
        "tokenId": token_id,
        "properties": {
            "files": [
                {
                    "uri": f"{token_id}.png",
                    "type": "image/png"
                }
            ]
        },
        "symbol": "NFT_COLLECTION"
    }
    return metadata

# Generate a list of attributes
def generate_attributes(layers):
    attributes = []
    for layer in layers:
        asset = choose_asset(layer)
        if asset is not None:  # If the chosen asset is not None, add it to attributes
            attribute_name = layer.capitalize()
            attribute_value = os.path.basename(asset).split('.')[0]  # Use the file name as the value
            attributes.append({
                "trait_type": attribute_name,
                "value": attribute_value
            })
    return attributes

# Function to generate the NFTs and metadata
def generate_nfts(num_nfts):
    nfts_metadata = []

    for token_id in range(1, num_nfts + 1):
        # Merge the layers to create the image
        merged_image = merge_assets(layer_order)
        image_filename = f"output/{token_id}.png"
        merged_image.save(image_filename)

        # Generate attributes and metadata
        attributes = generate_attributes(layer_order)
        metadata = generate_metadata(token_id, image_filename, attributes)

        # Save the metadata as a JSON file
        metadata_filename = f"output/{token_id}.json"
        with open(metadata_filename, 'w') as metadata_file:
            json.dump(metadata, metadata_file, indent=4)

        nfts_metadata.append(metadata)

    return nfts_metadata

# Example usage
generate_nfts(200)  # Create 200 NFTs

