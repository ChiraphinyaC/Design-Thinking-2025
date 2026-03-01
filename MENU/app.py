"""
app.py - Main Streamlit App for Food Menu Recommendation
เมนูวันนี้จากวัตถุดิบที่มี - Food Recipe Finder
"""

import streamlit as st
import pandas as pd
import time
from pathlib import Path
import json
import sys

# Add the 1 subdirectory to the path so we can import scrape_trueid
sys.path.insert(0, str(Path(__file__).parent / "1"))

from scrape_trueid import TrueIDFoodScraper

# Page configuration
st.set_page_config(
    page_title="🍽️ เมนูวันนี้จากวัตถุดิบที่มี",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 💾 DATA CACHING & LOADING
# ==========================================

RECIPES_CACHE_FILE = Path("recipes_cache.json")


def load_or_scrape_recipes(collection_url, max_recipes=50):
    """
    Load recipes from cache or scrape from TrueID Food
    
    Args:
        collection_url (str): TrueID collection/article URL
        max_recipes (int): Maximum number of recipes to scrape
        
    Returns:
        list: List of recipe dictionaries
    """
    # Try to load from cache first
    if RECIPES_CACHE_FILE.exists():
        try:
            with open(RECIPES_CACHE_FILE, 'r', encoding='utf-8') as f:
                recipes = json.load(f)
                if recipes:
                    st.success(f"✅ Loaded {len(recipes)} recipes from cache")
                    return recipes
        except:
            pass
    
    # If no cache, scrape from TrueID
    st.info("📡 Scraping recipes from TrueID Food website...")
    scraper = TrueIDFoodScraper()
    recipes = scraper.scrape_collection(collection_url, max_recipes)
    
    # Save to cache
    if recipes:
        with open(RECIPES_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(recipes, f, ensure_ascii=False, indent=2)
        st.success(f"✅ Scraped and cached {len(recipes)} recipes!")
    
    return recipes


@st.cache_data
def get_all_ingredients(recipes):
    """Extract and sort all unique ingredients from recipes"""
    all_ingredients = set()
    for recipe in recipes:
        for ing in recipe.get("ingredients", []):
            # Extract just the ingredient name (without amount)
            # e.g., "กระเทียม 1 ช้อนโต๊ะ" -> "กระเทียม"
            parts = ing.split()
            if parts:
                all_ingredients.add(parts[0])
    return sorted(list(all_ingredients))


def matches_criteria(recipe, selected_ingredients, search_query):
    """
    Check if a recipe matches the selected ingredients and search query
    
    Args:
        recipe (dict): Recipe data
        selected_ingredients (set): Selected ingredient names
        search_query (str): Search query string
        
    Returns:
        bool: True if recipe matches criteria
    """
    # Check search query
    if search_query:
        query_lower = search_query.lower()
        recipe_name = recipe.get("name", "").lower()
        ingredients_text = " ".join(recipe.get("ingredients", [])).lower()
        
        if query_lower not in recipe_name and query_lower not in ingredients_text:
            return False
    
    # Check ingredients
    if selected_ingredients:
        recipe_ingredients_text = " ".join(recipe.get("ingredients", [])).lower()
        
        # Check if any selected ingredient is in the recipe
        has_match = False
        for ing in selected_ingredients:
            if ing.lower() in recipe_ingredients_text:
                has_match = True
                break
        
        return has_match
    
    # If no filters, show all
    return True


def calculate_match_score(recipe, selected_ingredients):
    """
    Calculate how well a recipe matches the selected ingredients
    
    Args:
        recipe (dict): Recipe data
        selected_ingredients (set): Selected ingredient names
        
    Returns:
        float: Match score between 0 and 1
    """
    if not selected_ingredients:
        return 0
    
    recipe_ingredients_text = " ".join(recipe.get("ingredients", [])).lower()
    matches = 0
    
    for ing in selected_ingredients:
        if ing.lower() in recipe_ingredients_text:
            matches += 1
    
    return matches / len(selected_ingredients)


# ==========================================
# 🎨 UI LAYOUT
# ==========================================

st.title("🍽️ เมนูวันนี้จากวัตถุดิบที่มี")
# avoid nested double quotes by using single quotes inside
st.markdown("**'What's in My Kitchen?' - Find recipes based on ingredients you have**")

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Option to reload recipes
    if st.button("🔄 Reload Recipes from TrueID", use_container_width=True):
        if RECIPES_CACHE_FILE.exists():
            RECIPES_CACHE_FILE.unlink()
        st.cache_data.clear()
        st.rerun()
    
    st.divider()
    
    # Collection URL input
    collection_url = st.text_input(
        "TrueID Collection URL",
        value="https://food.trueid.net/detail/M6oyloE4klNB",
        help="URL of the TrueID article/collection page"
    )
    
    max_recipes = st.slider(
        "Number of recipes to scrape",
        min_value=5,
        max_value=100,
        value=20,
        step=5
    )

# Load recipes
try:
    recipes = load_or_scrape_recipes(collection_url, max_recipes)
    
    if not recipes:
        st.error("❌ Failed to load recipes. Please check the URL and try again.")
        st.stop()
    
except Exception as e:
    st.error(f"❌ Error: {str(e)}")
    st.stop()

# Main content area
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("🔍 Search & Filter")
    
    # Search box
    search_query = st.text_input(
        "Search by recipe name or ingredient:",
        placeholder="e.g., ไก่, ไข่, ผัด",
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Ingredient selection
    st.markdown("### 🥕 Select Ingredients You Have:")
    
    all_ingredients = get_all_ingredients(recipes)
    
    selected_ingredients = st.multiselect(
        "Choose ingredients:",
        options=all_ingredients,
        label_visibility="collapsed"
    )

with col2:
    # Results section
    filtered_recipes = [
        r for r in recipes
        if matches_criteria(r, set(selected_ingredients), search_query)
    ]
    
    # Sort by match score
    if selected_ingredients:
        filtered_recipes.sort(
            key=lambda r: calculate_match_score(r, set(selected_ingredients)),
            reverse=True
        )
    
    st.subheader(f"📋 Results ({len(filtered_recipes)} recipes)")
    
    if not filtered_recipes:
        st.info("❌ No recipes found matching your criteria. Try different ingredients!")
    else:
        # Display recipes in grid
        cols = st.columns(2)
        
        for idx, recipe in enumerate(filtered_recipes):
            with cols[idx % 2]:
                with st.container(border=True):
                    # Recipe name
                    st.markdown(f"### {recipe['name']}")
                    
                    # Match score if ingredients selected
                    if selected_ingredients:
                        score = calculate_match_score(recipe, set(selected_ingredients))
                        st.progress(
                            value=score,
                            text=f"Match: {score*100:.0f}%"
                        )
                        st.divider()
                    
                    # Display details in tabs
                    tab1, tab2, tab3 = st.tabs(["🥕 Ingredients", "📖 Steps", "ℹ️ Info"])
                    
                    with tab1:
                        st.markdown("**Ingredients:**")
                        for ing in recipe.get("ingredients", []):
                            # Highlight selected ingredients
                            ing_lower = ing.lower()
                            is_selected = any(s.lower() in ing_lower for s in selected_ingredients)
                            
                            if is_selected:
                                st.success(f"✅ {ing}")
                            else:
                                st.write(f"- {ing}")
                    
                    with tab2:
                        steps = recipe.get("steps", [])
                        if steps:
                            for step in steps:
                                st.write(step)
                        else:
                            st.info("Steps not available. Visit the website for detailed instructions.")
                    
                    with tab3:
                        col_a, col_b = st.columns([1, 1])
                        
                        with col_a:
                            st.write(f"**Difficulty:** {recipe.get('difficulty', 'ไม่ระบุ')}")
                            st.write(f"**Time:** {recipe.get('time', 'ไม่ระบุ')}")
                        
                        with col_b:
                            if st.button(
                                "🌐 View on TrueID",
                                key=f"url_{recipe.get('url', idx)}",
                                use_container_width=True
                            ):
                                st.write(recipe.get('url', 'N/A'))

# Footer
st.divider()
st.markdown("""
---
**💡 Tips:**
- Select multiple ingredients to find recipes that use them
- Use the search box to find specific recipes
- Click ingredient tabs to see all required ingredients
- Use the Settings sidebar to change the recipe source

**📊 Data Source:** TrueID Food (food.trueid.net)

**🤝 Team:** Nithis Baiaya & Jiraphunya Chaichomphu
""")
