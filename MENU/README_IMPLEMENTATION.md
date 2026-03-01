# 🍽️ เมนูวันนี้จากวัตถุดิบที่มี (What's in My Kitchen?)

## 📋 Project Description

A web application that helps users find recipes based on ingredients they have at home. The app scrapes recipe data from the TrueID Food website (food.trueid.net) and provides an interactive interface to search and discover recipes.

### ภาษาไทย
アプリケーションは、ユーザーが持っている食材に基づいてレシピを見つけるのに役立つWebアプリケーションです。このアプリはTrueID Foodウェブサイト（food.trueid.net）からレシピデータをスクレイプし、レシピを検索および発見するための対話型インターフェースを提供します。

## 🎯 Features

- **🔍 Smart Recipe Search**: Find recipes based on ingredients you have
- **📱 Interactive UI**: Easy-to-use Streamlit interface
- **⭐ Ingredient Matching**: Automatically highlights which recipes use your selected ingredients
- **📊 Match Scoring**: Shows how well each recipe matches your available ingredients
- **💾 Recipe Caching**: Recipes are cached for faster subsequent loads
- **🌐 TrueID Integration**: Scrapes recipe data directly from food.trueid.net

## 🛠️ Tech Stack

- **Backend**: Python
- **Frontend**: Streamlit (Web Framework)
- **Web Scraping**: BeautifulSoup 4, Requests
- **Data Processing**: Pandas, JSON

## 📁 Project Structure

```
MENU/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── preload_recipes.py             # Script to pre-load recipes
├── recipes_cache.json             # Cached recipe data
├── pages/
│   └── recipe_page.py             # Recipe detail page (future use)
└── 1/
    ├── scrape_trueid.py           # TrueID Food scraper module
    ├── scraper.py                 # Original Kapook scraper
    ├── scrape_kapook.py           # Kapook scraper variant
    ├── scrape_runner.py           # Scraper runner script
    ├── test_scrape.py             # Test script
    ├── recipe_output.csv          # CSV output from scraper
    └── recipes_dataset.csv        # Recipe dataset
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Navigate to the project directory:**
```bash
cd /workspaces/Design-Thinking-2025/MENU
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Pre-load recipes (optional but recommended):**
```bash
python preload_recipes.py
```

This will scrape 30 recipes from TrueID Food and cache them locally.

### Running the Application

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## 📖 User Guide

### How to Use the Application

1. **View Recipes**: The app displays all loaded recipes by default
2. **Search**: Use the search box to find recipes by name or ingredient
3. **Select Ingredients**: Choose ingredients you have from the multiselect list
4. **View Results**: See matching recipes with match scores
5. **Review Details**: Click on each recipe to see:
   - **Ingredients Tab**: Complete ingredient list with amounts
   - **Steps Tab**: Cooking instructions
   - **Info Tab**: Difficulty level, cooking time, and link to original source

### Filter & Search Options

- **Search Box**: Type ingredient or recipe names
- **Ingredient Selector**: Multi-select from available ingredients
- **Reload Button**: Fetch fresh recipes from TrueID Food

## 🔧 Configuration

### Settings (Sidebar)

- **Reload Recipes**: Clear cache and fetch new recipes from TrueID
- **Collection URL**: Enter any TrueID article/collection URL
- **Max Recipes**: Control how many recipes to scrape (5-100)

### Default Configuration

```python
Default Collection URL: "https://food.trueid.net/detail/M6oyloE4klNB"
Default Max Recipes: 20
```

## 📡 API: TrueID Food Web Scraper

### TrueIDFoodScraper Class

#### Methods

**`scrape_recipe(url)`**
- Scrapes a single recipe from a TrueID Food recipe page
- Parameters:
  - `url` (str): Full recipe URL or recipe ID
- Returns: Recipe dictionary with name, ingredients, steps, etc.

**`extract_recipe_links(page_url)`**
- Extracts all recipe links from a collection/article page
- Parameters:
  - `page_url` (str): URL of collection page
- Returns: List of recipe URLs

**`scrape_collection(collection_url, max_recipes=20)`**
- Scrapes all recipes from a collection page
- Parameters:
  - `collection_url` (str): URL of collection/article
  - `max_recipes` (int): Maximum recipes to scrape
- Returns: List of recipe dictionaries

#### Usage Example

```python
from scrape_trueid import TrueIDFoodScraper

scraper = TrueIDFoodScraper()

# Scrape single recipe
recipe = scraper.scrape_recipe("https://food.trueid.net/detail/mA1Jl95bpQgx")

# Scrape collection
recipes = scraper.scrape_collection(
    "https://food.trueid.net/detail/M6oyloE4klNB",
    max_recipes=50
)
```

## 🗂️ Data Structure

### Recipe Dictionary

```python
{
    "name": "สูตรทำ ไข่เจียวผัดผงกะหรี่",
    "ingredients": [
        "กระเทียม 1 ช้อนโต๊ะ",
        "หอมใหญ่ 30 กรัม",
        "ต้นหอม 15 กรัม",
        # ... more ingredients
    ],
    "steps": [
        "1. เตรียมวัตถุดิบทั้งหมด",
        "2. ผ่าไข่ใส่ชาม",
        # ... more steps
    ],
    "url": "https://food.trueid.net/detail/...",
    "difficulty": "ง่าย",
    "time": "20 นาที"
}
```

## 💡 Development Notes

### Backend Scraper (`scrape_trueid.py`)

The scraper is designed to:
1. Extract recipe links from collection pages
2. Parse individual recipe pages
3. Extract recipe name, ingredients, and steps
4. Handle Thai cooking units (กรัม, ช้อน, ถ้วย, etc.)
5. Cache results for performance

### Ingredient Matching Algorithm

The app uses a simple substring matching approach:
- Extracts the first word of each ingredient as the core ingredient name
- Checks if any selected ingredient is contained in recipe ingredients
- Calculates match score as: (matched ingredients / total selected) × 100%

### Caching Strategy

- Recipes are cached in `recipes_cache.json`
- Cache is used on app startup for faster loading
- Users can reload from TrueID using the "Reload Recipes" button

## ⚡ Performance Tips

1. **First Run**: First run will take 1-2 minutes as it scrapes recipes
2. **Subsequent Runs**: Cached recipes load instantly
3. **Reload**: Pre-load recipes using `python preload_recipes.py`

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'scrape_trueid'"
**Solution**: Make sure you're running the script from the MENU directory

### Issue: No recipes are loading
**Solution**: 
1. Check internet connection
2. Verify the TrueID URL is accessible
3. Try running `python preload_recipes.py`

### Issue: Some recipes have missing steps
**Solution**: 
- The scraper extracts numbered steps when available
- Some recipes may only have video instructions on TrueID
- Visit the TrueID website for complete instructions

## 📝 Future Enhancements

- [ ] Add user recipe favorites/bookmarks
- [ ] Ingredient amount matching
- [ ] Recipe rating/reviews
- [ ] Filter by difficulty or cooking time
- [ ] Shopping list generation
- [ ] Database backend for persistent storage
- [ ] Multi-source recipe scraping
- [ ] Recipe categorization (Thai, International, Desserts, etc.)

## 👥 Team Members & Responsibilities

| Member | Role |
|--------|------|
| Nithis Baiaya (นายณิธิศ ใบยา) | Backend & Scraper Development |
| Jiraphunya Chaichomphu (นางสาวจิรภิญญา ชัยชมภู) | Frontend & UI Development |

## 📄 License

This project is created for educational purposes.

## 📚 References

- [Streamlit Documentation](https://docs.streamlit.io/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [TrueID Food Website](https://food.trueid.net/)

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements!

---

**Last Updated**: March 2026  
**Status**: Active Development
