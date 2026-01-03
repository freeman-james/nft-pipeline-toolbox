import os

# Define the paths to your asset folders
asset_folders = [
    'assets/Accessory',
    'assets/Background',
    'assets/Body',
    'assets/Eyes',
    'assets/Head'
]

# Function to list all files in the folders
def list_files_in_folders(folders):
    all_files = {}
    for folder in folders:
        if os.path.exists(folder):
            all_files[folder] = [file for file in os.listdir(folder) if file.endswith('.png')]
        else:
            print(f"Folder not found: {folder}")
    return all_files

# Get the list of files in each folder
asset_files = list_files_in_folders(asset_folders)

# Print the asset files for each folder
for folder, files in asset_files.items():
    print(f"Files in {folder}:")
    for file in files:
        print(f"  {file}")
