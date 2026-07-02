import os
import json

BASE_FOLDER = "images_HD"
product_names = []

if os.path.exists(BASE_FOLDER):
    folders = os.listdir(BASE_FOLDER)
    product_names = [folder for folder in folders if os.path.isdir(os.path.join(BASE_FOLDER, folder))]
    print(product_names)
    
    # Create JSON file
    output_data = {
        "base_folder": BASE_FOLDER,
        "folder_count": len(product_names),
        "folders": product_names
    }
    
    # Write to JSON file
    with open("folder_names_test.json", "w") as json_file:
        json.dump(output_data, json_file, indent=4)
    
    print(f"\nJSON file created: folder_names.json")
    
else:
    print("folder is not available")