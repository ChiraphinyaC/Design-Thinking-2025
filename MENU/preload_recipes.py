"""
preload_recipes.py - Pre-load recipes cache from TrueID Food
ตัวโหลดข้อมูลสูตรอาหารล่วงหน้า
"""

import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent / "1"))

from scrape_trueid import TrueIDFoodScraper


def preload_recipes(collection_url, max_recipes=30, output_file="recipes_cache.json"):
    """
    Pre-load recipes from TrueID and save to cache file
    
    Args:
        collection_url (str): TrueID collection URL
        max_recipes (int): Number of recipes to scrape
        output_file (str): Output cache file path
    """
    print("="*70)
    print("TrueID Food Recipe Pre-Loader")
    print("="*70)
    
    scraper = TrueIDFoodScraper()
    
    print(f"\n📡 Starting to scrape recipes...")
    print(f"   URL: {collection_url}")
    print(f"   Max recipes: {max_recipes}\n")
    
    recipes = scraper.scrape_collection(collection_url, max_recipes)
    
    if recipes:
        # Save to file
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(recipes, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Successfully saved {len(recipes)} recipes to {output_file}")
        
        # Show sample recipes
        print("\n📋 Sample Recipes:")
        for i, recipe in enumerate(recipes[:5], 1):
            print(f"\n  {i}. {recipe['name']}")
            print(f"     Ingredients: {len(recipe.get('ingredients', []))} items")
            print(f"     Steps: {len(recipe.get('steps', []))} items")
        
        if len(recipes) > 5:
            print(f"\n  ... and {len(recipes) - 5} more recipes")
    else:
        print("❌ Failed to scrape recipes!")
        return False
    
    return True


if __name__ == "__main__":
    # Default collection URL with 45 dinner recipes
    collection_url = "https://food.trueid.net/detail/M6oyloE4klNB"
    
    # Pre-load recipes
    success = preload_recipes(collection_url, max_recipes=30)
    
    if success:
        print("\n" + "="*70)
        print("✅ Pre-loading complete! You can now run the Streamlit app:")
        print("   streamlit run app.py")
        print("="*70)
