import csv
import os

# Input files
ORIGINAL_CSV = "woocommerce_batches\woocommerce_import_batch_2.csv"  # Your original full CSV
EXPORTED_CSV = "exported_products.csv"  # CSV exported from WooCommerce
OUTPUT_CSV = "failed_products.csv"  # Products that failed to import

def read_products_from_csv(filename, sku_column_name="SKU"):
    """Read products and return set of parent product SKUs"""
    products = set()
    
    try:
        with open(filename, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Get SKU
                sku = row.get(sku_column_name, '').strip()
                row_type = row.get('Type', '').strip()
                
                # Only track parent products (variable type)
                if row_type == 'variable' and sku:
                    products.add(sku)
        
        return products
    except FileNotFoundError:
        print(f"Error: {filename} not found!")
        return set()

def extract_failed_products():
    print("Reading original CSV...")
    
    # Read original CSV and build product groups
    product_groups = {}
    
    with open(ORIGINAL_CSV, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)  # FIXED: Read all rows first
        
        current_sku = None
        current_group = []
        
        for row in rows:
            row_type = row[1]  # Type column
            sku = row[2]  # SKU column
            
            if row_type == "variable":
                # Save previous group
                if current_sku and current_group:
                    product_groups[current_sku] = current_group
                
                # Start new group
                current_sku = sku
                current_group = [row]
            elif row_type == "variation":
                current_group.append(row)
        
        # Save last group
        if current_sku and current_group:
            product_groups[current_sku] = current_group
    
    original_skus = set(product_groups.keys())
    print(f"✓ Found {len(original_skus)} products in original CSV")
    
    # Read exported CSV
    print("Reading exported CSV...")
    exported_skus = read_products_from_csv(EXPORTED_CSV)
    print(f"✓ Found {len(exported_skus)} products in exported CSV")
    
    # Find failed products
    failed_skus = original_skus - exported_skus
    print(f"\n{'='*50}")
    print(f"Failed to import: {len(failed_skus)} products")
    print(f"Successfully imported: {len(exported_skus)} products")
    print(f"{'='*50}\n")
    
    if not failed_skus:
        print("✓ All products imported successfully!")
        return
    
    # Write failed products to new CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        
        for sku in sorted(failed_skus):
            if sku in product_groups:
                writer.writerows(product_groups[sku])
    
    print(f"✓ Failed products saved to: {OUTPUT_CSV}")
    print(f"✓ Total rows in failed CSV: {sum(len(product_groups[sku]) for sku in failed_skus)}")
    print("\nFailed product SKUs:")
    for sku in sorted(list(failed_skus)[:20]):  # Show first 20
        print(f"  - {sku}")
    
    if len(failed_skus) > 20:
        print(f"  ... and {len(failed_skus) - 20} more")

def extract_failed_products_fixed():
    print("Reading original CSV...")
    
    # Read original CSV and build product groups
    product_groups = {}
    
    with open(ORIGINAL_CSV, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
        
        current_sku = None
        current_group = []
        
        for row in rows:
            row_type = row[1]  # Type column
            sku = row[2]  # SKU column
            
            if row_type == "variable":
                # Save previous group
                if current_sku and current_group:
                    product_groups[current_sku] = current_group
                
                # Start new group
                current_sku = sku
                current_group = [row]
            elif row_type == "variation":
                current_group.append(row)
        
        # Save last group
        if current_sku and current_group:
            product_groups[current_sku] = current_group
    
    original_skus = set(product_groups.keys())
    print(f"✓ Found {len(original_skus)} products in original CSV")
    
    # Read exported CSV
    print("Reading exported CSV...")
    exported_skus = read_products_from_csv(EXPORTED_CSV)
    print(f"✓ Found {len(exported_skus)} products in exported CSV")
    
    # Find failed products
    failed_skus = original_skus - exported_skus
    print(f"\n{'='*50}")
    print(f"Failed to import: {len(failed_skus)} products")
    print(f"Successfully imported: {len(exported_skus)} products")
    print(f"{'='*50}\n")
    
    if not failed_skus:
        print("✓ All products imported successfully!")
        return
    
    # Write failed products to new CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        
        for sku in sorted(failed_skus):
            if sku in product_groups:
                writer.writerows(product_groups[sku])
    
    print(f"✓ Failed products saved to: {OUTPUT_CSV}")
    print(f"✓ Total rows in failed CSV: {sum(len(product_groups[sku]) for sku in failed_skus)}")
    print("\nFailed product SKUs (first 20):")
    for sku in sorted(list(failed_skus)[:20]):
        print(f"  - {sku}")
    
    if len(failed_skus) > 20:
        print(f"  ... and {len(failed_skus) - 20} more")

if __name__ == "__main__":
    extract_failed_products()