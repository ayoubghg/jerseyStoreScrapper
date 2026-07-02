import os
import csv
from PIL import Image
from contry_continent import COUNTRY_TO_CONTINENT, SIZES, BASE_FOLDER

BASE_URL = "https://offsidejersey.shop/wp-content/uploads/2026_World_Cup"
OUTPUT_CSV = "woocommerce_import_world_cup_26.csv"


def extract_country(foldername):
    parts = foldername.split("_")
    for part in parts:
        if part in COUNTRY_TO_CONTINENT:
            return part
    return ""


def get_continent(country):
    return COUNTRY_TO_CONTINENT.get(country, "")


def build_categories(country):
    continent = get_continent(country)
    if not country or not continent:
        return ""
    return f"FOOTBALL JERSEYS > National > {continent}, FOOTBALL JERSEYS > National > {continent} > {country}"


def build_image_urls(product_folder):
    """Return all images + detect best 800x800 first image."""
    
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
        except:
            pass

        images.append(url)

    # If no 800x800 image: fallback to first image
    if main_image is None and images:
        main_image = images[0]

    return main_image, images


def main():
    product_folders = [
        f for f in os.listdir(BASE_FOLDER)
        if os.path.isdir(os.path.join(BASE_FOLDER, f))
    ]

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
            "Stock status"
        ])

        for folder in product_folders:

            product_name = folder.replace("_", " ")
            country = extract_country(folder)
            continent = get_continent(country)

            if not country or not continent:
                continue

            categories = build_categories(country)

            # NEW: detect first 800x800 image
            main_image, all_images = build_image_urls(folder)

            images_joined = ", ".join([main_image] + [img for img in all_images if img != main_image])

            # Parent product
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
                    "300", images_joined, "", folder,
                    "Size", size,
                    1, 1, "",
                    "instock"
                ])

    print("Done:", OUTPUT_CSV)


if __name__ == "__main__":
    main()
