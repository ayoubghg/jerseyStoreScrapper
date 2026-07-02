import os
import csv
import json
from PIL import Image

SIZES = ["S", "M", "L", "XL", "XXL"]
BASE_FOLDER = "images_HD"
BASE_URL = f"https://offsidejersey.shop/wp-content/uploads/{BASE_FOLDER}"
OUTPUT_CSV = "woocommerce_import_retro.csv"
PRODUCTS_JSON = "wind_clean.json"
price=500


def load_products_json(json_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_file} not found.")
        return None


def build_image_urls(product_folder, base_folder, base_url):
    folder_path = os.path.join(base_folder, product_folder)
    images = []
    main_image = None

    if not os.path.isdir(folder_path):
        return "", []

    for fname in sorted(os.listdir(folder_path)):
        if not fname.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            continue

        file_path = os.path.join(folder_path, fname)
        url = f"{base_url}/{product_folder}/{fname}"

        try:
            with Image.open(file_path) as img:
                w, h = img.size
                if w == 800 and h == 800 and main_image is None:
                    main_image = url
        except:
            pass

        images.append(url)

    if main_image is None and images:
        main_image = images[0]

    return main_image, images


def main():
    products_data = load_products_json(PRODUCTS_JSON)
    if not products_data:
        return

    products = products_data.get('products', [])
    base_folder = products_data.get('base_folder', BASE_FOLDER)

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)

        writer.writerow([
            "ID", "Type", "SKU", "Name", "Published",
            "Is featured?", "Visibility in catalog",
            "Description", "Short description",
            "Tax status", "In stock?", "Manage stock?",
            "Backorders allowed?", "Sold individually?",
            "Regular price", "Categories", "Images",
            "Parent",
            "Attribute 1 name", "Attribute 1 value(s)",
            "Attribute 1 visible", "Attribute 1 global",
            "Attribute 1 default",
            "Stock"   
        ])

        for product in products:
            original_name = product['original_name']
            clean_name = product['clean_name']
            category = product['category']

            if not category:
                continue

            main_image, all_images = build_image_urls(original_name, base_folder, BASE_URL)
            images_joined = ", ".join([main_image] + [img for img in all_images if img != main_image])

      
            writer.writerow([
                "", "variable", original_name, clean_name, 1,
                0, "visible",
                clean_name, clean_name,
                "taxable", 1, "no",
                "no", "no",
                "", category, images_joined,
                "",
                "Size", ", ".join(SIZES),
                1, 1, SIZES[0],
                "instock"  # FIXED
            ])

            
            for size in SIZES:
                sku = f"{original_name}-{size}"

                writer.writerow([
                    "", "variation", sku, "", 1,
                    0, "visible",
                    "", "",
                    "taxable", "", "no", 
                    "no", "no",
                    f"{price}", category, images_joined, original_name,
                    "Size", size,
                    1, 1, "",
                    "instock"  
                ])

    print("✓ CSV generated successfully.")
    print("✓ All products and variations will now be IN STOCK.")


if __name__ == "__main__":
    main()
