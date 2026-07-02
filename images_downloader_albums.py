import os
import csv
import json
from PIL import Image

# Configuration
SIZES = ["S", "M", "L", "XL", "XXL"]
BASE_FOLDER = "wind"  # Your base folder path
BASE_URL = f"https://offsidejersey.shop/wp-content/uploads/{BASE_FOLDER}"
OUTPUT_CSV = "woocommerce_import_wind.csv"
PRODUCTS_JSON = "wind_clean.json"
price=500

def load_products_json(json_file):
    """Load the cleaned products JSON"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_file} not found.")
        return None


def build_image_urls(product_folder, base_folder, base_url):
    """Return all images + detect best 800x800 first image."""
    
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

        # Check resolution for the main image
        try:
            with Image.open(file_path) as img:
                w, h = img.size
                if w == 800 and h == 800 and main_image is None:
                    main_image = url
        except:
            pass

        images.append(url)

    # If no 800x800 image: fallback to first image
    if main_image is None and images:
        main_image = images[0]

    return main_image, images


def main():
    # Load products from JSON
    products_data = load_products_json(PRODUCTS_JSON)
    if not products_data:
        return
    
    products = products_data.get('products', [])
    base_folder = products_data.get('base_folder', BASE_FOLDER)
    
    print(f"Processing {len(products)} products...")
    
    # Track statistics
    processed = 0
    skipped = 0

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)

        # Write header
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

        for product in products:
            original_name = product['original_name']
            clean_name = product['clean_name']
            category = product['category']
            
            # Skip products without category
            if not category:
                skipped += 1
                continue

            # Get images
            main_image, all_images = build_image_urls(original_name, base_folder, BASE_URL)
            
            if not all_images:
                print(f"Warning: No images found for {original_name}")
            
            images_joined = ", ".join([main_image] + [img for img in all_images if img != main_image])

            # Parent product
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
                "instock"
            ])

            # Variations
            for size in SIZES:
                sku = f"{original_name}-{size}"

                writer.writerow([
                    "", "variation", sku, "", 1,
                    0, "visible",
                    "", "",
                    "taxable", 1, "no",
                    "no", "no",
                    price, category, images_joined, original_name,
                    "Size", size,
                    1, 1, "",
                    "instock"
                ])
            
            processed += 1

    print(f"\n✓ Done: {OUTPUT_CSV}")
    print(f"✓ Processed: {processed} products")
    print(f"✓ Skipped (no category): {skipped} products")


if __name__ == "__main__":
    main()