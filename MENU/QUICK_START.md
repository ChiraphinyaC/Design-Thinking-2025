# 🍽️ เมนูวันนี้จากวัตถุดิบที่มี - Quick Start Guide

## ✨ What You've Built

A food recipe finder web application that:
- 🔍 Searches for recipes based on ingredients you have
- 📱 Uses Streamlit for an interactive web interface  
- 📡 Scrapes recipe data from TrueID Food website
- 💾 Caches recipes locally for fast loading
- ⭐ Shows ingredient match scores

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
cd /workspaces/Design-Thinking-2025/MENU
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
streamlit run app.py
```

The app will open at: `http://localhost:8501`

### Step 3: Use the App
1. Open the app in your browser
2. Click the sidebar Settings button if you want to adjust options
3. Select ingredients you have from the list
4. Browse matching recipes
5. Click on a recipe to see ingredients and steps

## 📦 Project Files Overview

### Core Files
| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit application |
| `requirements.txt` | Python dependencies |
| `recipes_cache.json` | Cached recipe data (pre-loaded) |

### Scraper Module
| File | Purpose |
|------|---------|
| `1/scrape_trueid.py` | TrueID Food scraper class |
| `preload_recipes.py` | Script to load recipes |

### Documentation
| File | Purpose |
|------|---------|
| `README_IMPLEMENTATION.md` | Complete project documentation |
| `QUICK_START.md` | This file |

## 🎯 Key Features Implemented

✅ **Web Scraping**
- Extracts recipes from TrueID Food
- Handles collection pages with multiple recipes
- Parses ingredients, steps, cooking time, difficulty

✅ **User Interface**
- Search by recipe name or ingredient
- Multi-select ingredient picker
- Match score calculation (shows % match)
- Tabbed recipe details view

✅ **Caching System**
- Recipes cached in JSON format
- Loads from cache on startup
- Reload button to fetch fresh data

✅ **Ingredient Matching**
- Highlights selected ingredients in recipes
- Shows match percentage
- Results sorted by relevance

## 💡 Common Tasks

### View All Available Recipes
Just open the app - all recipes display by default

### Find Recipes with Specific Ingredients
1. Open the app
2. In the "Select Ingredients" section, choose the ingredients you have
3. The results will filter automatically

### Search by Recipe Name
1. Type in the search box at the top
2. Results filter as you type

### Reload Recipes from TrueID
1. Click the "🔄 Reload Recipes from TrueID" button in the sidebar
2. This will fetch fresh recipes from the website

### Change the Recipe Source
1. In the Settings sidebar, find "TrueID Collection URL"
2. Copy any TrueID article/collection URL
3. The app will load recipes from that collection

## 📊 Data Architecture

```
User Interface (Streamlit)
           ↓
    Main App (app.py)
           ↓
    Recipe Cache (JSON)  ← or → TrueID Web Scraper
           ↓
    Display with Filters & Matching
```

## 🔧 Customization Ideas

### Add More Initial Recipes
```bash
# Edit preload_recipes.py
# Change max_recipes value and run:
python preload_recipes.py
```

### Change Default Search URL
```python
# In app.py, look for the default value:
collection_url = st.text_input(
    "TrueID Collection URL",
    value="YOUR_NEW_URL_HERE",  # <- Change this
```

### Adjust Ingredient Matching Logic
Edit the `calculate_match_score()` function in app.py

## ⚙️ System Requirements

- Python 3.8+
- Internet connection (for first run/scraping)
- ~100MB disk space for cache
- Any modern web browser

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "No recipes loading" | Check internet; Try clicking "Reload Recipes" |
| "Module not found" | Ensure you're in `/MENU` directory |
| "App won't start" | Check Python version (need 3.8+) |
| "Very slow on first run" | Normal - scraping takes time. Use preload instead |

## 📝 Development Tips

### Test the Scraper Directly
```bash
cd 1/
python scrape_trueid.py
```

### Pre-load Recipes from Command Line
```bash
python preload_recipes.py
```

### Clear Cache and Start Fresh
```bash
rm recipes_cache.json
streamlit run app.py
```

## 🎓 Learning Resources

The project demonstrates:
- **Web Scraping**: BeautifulSoup, Requests
- **Web Framework**: Streamlit basics
- **Data Processing**: JSON, filtering, sorting
- **Python**: Functions, caching, string matching

## 🤝 Next Steps

### Potential Improvements
1. ✨ Add recipe ratings/reviews
2. 🔖 Implement bookmarking system
3. 📸 Add recipe images from TrueID
4. 💾 Switch to database backend
5. 🌐 Support multiple recipe sources
6. 🍽️ Add nutrition information
7. 📱 Create mobile app version
8. 🔄 Auto-refresh recipes periodically

### Project Extensions
- Create an API for mobile apps
- Add recipe export (PDF, print)
- Implement user accounts & preferences
- Build shopping list feature

## 📞 Support

For issues or questions:
1. Check `README_IMPLEMENTATION.md` for detailed docs
2. Review the code comments
3. Test the scraper: `python 1/scrape_trueid.py`

---

**Happy Cooking! 🍳** 

Made with ❤️ by the team
