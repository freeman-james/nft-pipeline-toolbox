import random
from PIL import Image
import json
import os

# Define paths to your assets (populated based on the folders you listed)
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
        'assets/Head/Straw Hat.png',  # Straw Hat head
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

# To track unique combinations
generated_combinations = set()

# Function to choose an asset based on rarity
def choose_asset(layer):
    weight = rarity_weights[layer]
    chosen_index = random.choices(range(len(asset_paths[layer])), weights=weight, k=1)[0]
    return asset_paths[layer][chosen_index]

# Function to merge assets
def merge_assets_from_metadata(metadata):
    # Start with the background layer
    base_image = Image.open(metadata['asset_paths']['background'])
    
    # Iterate through the layers in the metadata
    for layer in ['body', 'head', 'eyes', 'accessory']:
        asset_path = metadata['asset_paths'].get(layer)
        if asset_path:
            asset_image = Image.open(asset_path)
            base_image.paste(asset_image, (0, 0), asset_image)  # Assuming assets are transparent PNGs

    return base_image

# Function to generate metadata for the NFT
def generate_metadata(token_id, attributes, asset_paths_dict):
    metadata = {
        "name": f"YACHTBOT #{token_id}",
        "description": "Botz on Yachtz",
        "external_url": "https://yachbotz.xyz",  # project website
        "image": f"ipfs://ipfs-url/{token_id}.png",  # IPFS URL for the image will be updated later
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
        "symbol": "YACHTBOTZ",
        "asset_paths": asset_paths_dict  # Store the asset paths for each layer in the metadata
    }
    return metadata

# Generate a list of attributes
def generate_attributes(layers):
    attributes = []
    asset_paths_dict = {}
    for layer in layers:
        asset = choose_asset(layer)
        if asset is not None:  # If the chosen asset is not None, add it to attributes
            attribute_name = layer.capitalize()
            attribute_value = os.path.basename(asset).split('.')[0]  # Use the file name as the value
            attributes.append({
                "trait_type": attribute_name,
                "value": attribute_value
            })
            asset_paths_dict[layer] = asset  # Track the exact asset path used for each layer
    return attributes, asset_paths_dict

# Step 1: Generate Metadata First and Save to Folder
def generate_metadata_for_all_nfts(num_nfts, metadata_folder='output/metadata'):
    if not os.path.exists(metadata_folder):
        os.makedirs(metadata_folder)

    nfts_metadata = []
    
    for token_id in range(1, num_nfts + 1):
        while True:
            # Generate unique attributes by checking combinations
            attributes, asset_paths_dict = generate_attributes(layer_order)
            combination = tuple([attr['value'] for attr in attributes])
            
            # Ensure that this combination has not been generated already
            if combination not in generated_combinations:
                # Mark this combination as used
                generated_combinations.add(combination)

                # Generate metadata
                metadata = generate_metadata(token_id, attributes, asset_paths_dict)
                metadata_filename = os.path.join(metadata_folder, f"{token_id}.json")
                
                # Save the metadata file
                with open(metadata_filename, 'w') as metadata_file:
                    json.dump(metadata, metadata_file, indent=4)
                
                nfts_metadata.append(metadata)
                print(f"Generated metadata for NFT #{token_id} with unique combination.")
                break  # Proceed to next NFT once we ensure it's unique

    return nfts_metadata

# Step 2: Read Metadata Files and Generate Images
def generate_images_from_metadata(metadata_folder='output/metadata'):
    metadata_files = os.listdir(metadata_folder)
    print("Reading metadata files...\n")

    for metadata_file in metadata_files:
        if metadata_file.endswith(".json"):
            metadata_filepath = os.path.join(metadata_folder, metadata_file)
            
            # Load the metadata
            with open(metadata_filepath, 'r') as metadata_file:
                metadata = json.load(metadata_file)
            
            # Print the metadata being read for debugging purposes
            print(f"Reading Metadata for NFT #{metadata['tokenId']}:")
            print(json.dumps(metadata, indent=4))  # Print the full metadata for the NFT

            # Merge the layers to create the image
            merged_image = merge_assets_from_metadata(metadata)
            token_id = metadata["tokenId"]
            image_filename = f"output/{token_id}.png"
            merged_image.save(image_filename)
            
            # Update the metadata with the correct image URL (IPFS URL)
            metadata["image"] = f"ipfs://ipfs-url/{token_id}.png"
            
            # Save the metadata with the updated image URL
            with open(metadata_filepath, 'w') as metadata_file:
                json.dump(metadata, metadata_file, indent=4)

            print(f"Generated image for NFT #{token_id} and updated metadata.")

# Example usage
generate_metadata_for_all_nfts(200)  # Step 1: Generate metadata for 200 NFTs and save to the folder
generate_images_from_metadata()  # Step 2: Read metadata files and generate images
