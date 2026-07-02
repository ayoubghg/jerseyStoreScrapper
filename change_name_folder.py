import os

# Path to the main folder containing subfolders
main_folder = "images_HD"

# Iterate through all items in the main folder
for folder_name in os.listdir(main_folder):
    folder_path = os.path.join(main_folder, folder_name)
    
    # Check if it's a folder
    if os.path.isdir(folder_path):
        # Create new folder name by replacing spaces with underscores
        new_folder_name = folder_name.replace(" ", "_")
        new_folder_path = os.path.join(main_folder, new_folder_name)
        
        # Rename the folder if the new name is different
        if new_folder_name != folder_name:
            os.rename(folder_path, new_folder_path)
            print(f"Renamed '{folder_name}' -> '{new_folder_name}'")
