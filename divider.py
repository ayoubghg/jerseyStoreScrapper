import csv
import os

INPUT_CSV = "woocommerce_import_retro.csv"
OUTPUT_FOLDER = "woocommerce_batches"
PRODUCTS_PER_FILE = 300  # Number of parent products per batch

def divide_csv():
    # Create output folder
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    with open(INPUT_CSV, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = next(reader)  # Read header
        
        rows = list(reader)
    
    print(f"Total rows in CSV: {len(rows)}")
    
    # Group rows by parent product
    product_groups = []
    current_group = []
    
    for row in rows:
        row_type = row[1]  # Type column (variable/variation)
        
        if row_type == "variable":
            # Start new product group
            if current_group:
                product_groups.append(current_group)
            current_group = [row]
        elif row_type == "variation":
            # Add variation to current group
            current_group.append(row)
    
    # Don't forget the last group
    if current_group:
        product_groups.append(current_group)
    
    print(f"Total products found: {len(product_groups)}")
    print(f"Products per file: {PRODUCTS_PER_FILE}")
    print(f"Files to create: {(len(product_groups) + PRODUCTS_PER_FILE - 1) // PRODUCTS_PER_FILE}")
    print("-" * 50)
    
    # Write batches
    file_count = 0
    
    for i in range(0, len(product_groups), PRODUCTS_PER_FILE):
        file_count += 1
        batch = product_groups[i:i + PRODUCTS_PER_FILE]
        
        filename = os.path.join(OUTPUT_FOLDER, f"woocommerce_import_batch_{file_count}.csv")
        
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(header)  # Write header
            
            # Write all rows for products in this batch
            for product_group in batch:
                writer.writerows(product_group)
        
        products_in_batch = len(batch)
        rows_in_batch = sum(len(group) for group in batch)
        print(f"✓ Batch {file_count} created: {products_in_batch} products ({rows_in_batch} rows) -> {filename}")
    
    print("-" * 50)
    print(f"✓ Successfully created {file_count} CSV files in '{OUTPUT_FOLDER}' folder")
    print(f"\nImport them in order: batch_1.csv, then batch_2.csv, etc.")

if __name__ == "__main__":
    divide_csv()