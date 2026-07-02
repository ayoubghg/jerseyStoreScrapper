import json
import re

def normalize_text(text):
    """Normalize text for comparison"""
    replacements = {
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'á': 'a', 'à': 'a', 'â': 'a', 'ä': 'a', 'ã': 'a',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'ó': 'o', 'ò': 'o', 'ô': 'o', 'ö': 'o', 'õ': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c', 'ñ': 'n', 'ş': 's', 'ğ': 'g', 'ö': 'o'
    }
    text = text.lower()
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def load_teams_data(teams_json_file):
    """Load the teams JSON file"""
    try:
        with open(teams_json_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {teams_json_file} not found.")
        return {}

def create_category_map(teams_data):
    """Create a map of normalized team names for matching"""
    cat_map = {}
    
    for team_name, league in teams_data.items():
        normalized = normalize_text(team_name)
        
        # Store various versions for flexible matching
        cat_map[normalized] = {
            'team': team_name,
            'league': league
        }
        cat_map[normalized.replace(' ', '_')] = {
            'team': team_name,
            'league': league
        }
        cat_map[normalized.replace(' ', '')] = {
            'team': team_name,
            'league': league
        }
        # Also store with dashes
        cat_map[normalized.replace(' ', '-')] = {
            'team': team_name,
            'league': league
        }
    
    return cat_map

def clean_product_name(folder_name):
    """Clean the product name by removing size info and underscores"""
    # Remove size patterns
    cleaned = re.sub(r'_[Ss]-\d*X*[Ll]', '', folder_name)
    cleaned = re.sub(r'_\d+-\d+', '', cleaned)
    
    # Replace underscores with spaces
    cleaned = cleaned.replace('_', ' ')
    
    # Clean up extra spaces
    cleaned = ' '.join(cleaned.split())
    
    return cleaned

def extract_category(folder_name, cat_map):
    """Extract team/category from folder name"""
    folder_normalized = normalize_text(folder_name)
    
    # Sort categories by length (longest first) for better matching
    sorted_cats = sorted(cat_map.items(), key=lambda x: len(x[0]), reverse=True)
    
    # Try to find exact matches first
    for normalized_cat, team_info in sorted_cats:
        if normalized_cat in folder_normalized:
            team_name = team_info['team']
            league = team_info['league']
            # Format: "FOOTBALL JERSEYS > {league} > {team_name}"
            return f"FOOTBALL JERSEYS > {league} > {team_name} , Windbreaker "
    
    # If no match, return empty string
    return "Windbreaker"

def process_products(json_file, teams_json_file, output_file):
    """Process the products JSON and create cleaned version"""
    
    # Load teams data
    teams_data = load_teams_data(teams_json_file)
    if not teams_data:
        return
    
    # Create category mapping
    cat_map = create_category_map(teams_data)
    
    # Load products JSON
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: {json_file} not found.")
        return
    
    products = []
    folder_names = data.get('folders', [])
    
    print(f"Processing {len(folder_names)} products...")
    
    for folder_name in folder_names:
        clean_name = clean_product_name(folder_name)
        category = extract_category(folder_name, cat_map)
        
        product = {
            'original_name': folder_name,
            'clean_name': clean_name,
            'category': category
        }
        products.append(product)
    
    # Create output JSON
    output_data = {
        'total_products': len(products),
        'base_folder': data.get('base_folder', 'Retro'),
        'products': products
    }
    
    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(output_data, file, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Successfully processed {len(products)} products")
    print(f"✓ Output saved to: {output_file}")
    
    # Show category distribution
    category_count = {}
    uncategorized = 0
    for product in products:
        cat = product['category']
        if cat:
            category_count[cat] = category_count.get(cat, 0) + 1
        else:
            uncategorized += 1
    
    print(f"\nFound {len(category_count)} different categories")
    print(f"Uncategorized products: {uncategorized}")
    
    print("\nTop 10 categories:")
    for cat, count in sorted(category_count.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {cat}: {count} products")
    
    # Show some examples
    print("\nExample products:")
    for i, product in enumerate(products[:5]):
        print(f"\n{i+1}. Original: {product['original_name']}")
        print(f"   Clean: {product['clean_name']}")
        print(f"   Category: {product['category']}")

# Usage
if __name__ == "__main__":
    json_file = "folder_names_test.json"  # Your input JSON file with folders
    teams_json_file = "teams_leagues.json"  # Your teams JSON file (the one you provided)
    output_file = "wind_clean.json"  # Output file
    
    process_products(json_file, teams_json_file, output_file)