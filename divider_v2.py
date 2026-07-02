import csv
import os

INPUT_FOLDER = "./"        
OUTPUT_FOLDER = "woocommerce_batches_50"    
PRODUCTS_PER_FILE = 50                      

def split_batches():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Get all CSV files in INPUT_FOLDER
    batch_files = sorted([
        f for f in os.listdir(INPUT_FOLDER)
        if f.lower().endswith(".csv")
    ])

    if not batch_files:
        print("❌ No CSV files found in", INPUT_FOLDER)
        return

    file_counter = 0
    print(f"Found {len(batch_files)} batch files to split.")
    print("-" * 50)

    for batch_file in batch_files:
        path = os.path.join(INPUT_FOLDER, batch_file)

        # --- Load CSV ---
        with open(path, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = list(reader)

        # --- Group rows into products ---
        product_groups = []
        current_group = []

        for row in rows:
            row_type = row[1].strip().lower()  # column "Type" (variable / variation)

            if row_type == "variable":
                # Start a new product group
                if current_group:
                    product_groups.append(current_group)
                current_group = [row]

            elif row_type == "variation":
                # Variation belongs to current product
                current_group.append(row)

        if current_group:
            product_groups.append(current_group)

        print(f"{batch_file}: {len(product_groups)} parent products found")

        # --- Split into 50-product batches ---
        for i in range(0, len(product_groups), PRODUCTS_PER_FILE):
            file_counter += 1
            new_batch = product_groups[i:i + PRODUCTS_PER_FILE]

            output_name = f"batch_50_{file_counter}.csv"
            output_path = os.path.join(OUTPUT_FOLDER, output_name)

            with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(header)

                for product in new_batch:
                    writer.writerows(product)

            rows_count = sum(len(group) for group in new_batch)
            print(f"✓ Created {output_name} — {len(new_batch)} products ({rows_count} rows)")

    print("-" * 50)
    print(f"✓ Finished. Total small batches created: {file_counter}")
    print(f"Output folder: {OUTPUT_FOLDER}")


if __name__ == "__main__":
    split_batches()
