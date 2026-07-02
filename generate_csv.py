import os
import csv
import json
from PIL import Image

# Configuration
BASE_FOLDER = "Retro"  # Base folder containing product folders
BASE_URL = "https://offsidejersey.shop/wp-content/uploads/Retro"
OUTPUT_CSV = "retro_products_import.csv"
PRODUCTS_JSON = "products_clean.json"
SIZES = ["S", "M", "L", "XL", "XXL"]

def load_cleaned_products(json_file):
    """Load the cleaned products JSON"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
           
            products_map = {}
            for product in data.get('products', []):
                products_map[product['original_name']] = product
            return products_map
    except FileNotFoundError:
        print(f"Warning: {json_file} not found. Using folder names as product names.")
        return {}


def build_categories(category):
    
    if not category:
        return "retro"
    return f"FOOTBALL JERSEYS > retro, {category}"


def build_image_urls(product_folder):
    """Return all images with 800x800 as main image if available"""
    folder_path = os.path.join(BASE_FOLDER, product_folder)
    images = []
    main_image = None

    if not os.path.isdir(folder_path):
        return "", []

    for fname in sorted(os.listdir(folder_path)):
        if not fname.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            continue

        file_path = os.path.join(folder_path, fname)
        url = f"{BASE_URL}/{product_folder}/{fname}"

        # Check resolution for the main image
        try:
            with Image.open(file_path) as img:
                w, h = img.size
                if w == 800 and h == 800 and main_image is None:
                    main_image = url
        except Exception as e:
            print(f"Warning: Could not read image {file_path}: {e}")
            pass

        images.append(url)

    # If no 800x800 image: fallback to first image
    if main_image is None and images:
        main_image = images[0]

    return main_image, images

def main():
    # Load cleaned products data
    products_data = load_cleaned_products(PRODUCTS_JSON)
    
    # Get all product folders
    if not os.path.exists(BASE_FOLDER):
        print(f"Error: Base folder '{BASE_FOLDER}' not found!")
        return
    
    product_folders = [
        f for f in os.listdir(BASE_FOLDER)
        if os.path.isdir(os.path.join(BASE_FOLDER, f))
    ]

    print(f"Found {len(product_folders)} product folders")
    print(f"Loaded {len(products_data)} cleaned product names")

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)

        # CSV Header
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
            "Stock status"
        ])

        processed_count = 0

        for folder in product_folders:
            # Get cleaned product data
            product_info = products_data.get(folder, {})
            product_name = product_info.get('clean_name', folder.replace("_", " "))
            category = product_info.get('category', 'retro')

            # Build categories
            categories = build_categories(category)

            # Get images (with 800x800 as main)
            main_image, all_images = build_image_urls(folder)

            if not all_images:
                print(f"Warning: No images found for {folder}")
                continue

            # Build images string (main image first)
            images_joined = ", ".join([main_image] + [img for img in all_images if img != main_image])

            # Parent product (variable)
            writer.writerow([
                "", "variable", folder, product_name, 1,
                0, "visible",
                product_name, product_name,
                "taxable", 1, "no",
                "no", "no",
                "", categories, images_joined,
                "",
                "Size", ", ".join(SIZES),
                1, 1, SIZES[0],
                "instock"
            ])

            # Variations
            for size in SIZES:
                sku = f"{folder}-{size}"

                writer.writerow([
                    "", "variation", sku, "", 1,
                    0, "visible",
                    "", "",
                    "taxable", 1, "no",
                    "no", "no",
                    "300", "", images_joined, folder,
                    "Size", size,
                    1, 1, "",
                    "instock"
                ])

            processed_count += 1

    print(f"\n✓ Successfully processed {processed_count} products")
    print(f"✓ CSV file created: {OUTPUT_CSV}")
    print(f"✓ Total rows (parent + variations): {processed_count * (1 + len(SIZES))}")

if __name__ == "__main__":
    main()