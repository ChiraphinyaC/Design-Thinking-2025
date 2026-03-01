"""
scrape_trueid.py : Scraper for TrueID Food website (food.trueid.net)
ตัวดึงข้อมูลสูตรอาหารจากเว็บไซต์ food.trueid.net
"""
import requests
from bs4 import BeautifulSoup
import json
import re
import time


class TrueIDFoodScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.base_url = "https://food.trueid.net"
    
    def extract_recipe_links(self, page_url):
        """
        Extract recipe links from a collection/article page
        
        Args:
            page_url (str): URL of collection page
            
        Returns:
            list: List of recipe URLs
        """
        try:
            response = requests.get(page_url, headers=self.headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            recipe_links = []
            for link in soup.find_all("a", href=True):
                href = link.get('href', '')
                text = link.get_text(strip=True)
                
                # Match TrueID recipe links
                if 'food.trueid.net/detail/' in href and text and len(text) > 3:
                    # Ensure full URL
                    if not href.startswith('http'):
                        href = f"{self.base_url}{href}"
                    # Remove URL parameters
                    if '?' in href:
                        href = href.split('?')[0]
                    
                    if href not in recipe_links:
                        recipe_links.append(href)
            
            print(f"✅ Found {len(recipe_links)} recipe links")
            return recipe_links
            
        except Exception as e:
            print(f"❌ Error extracting recipe links: {str(e)}")
            return []
    
    def scrape_recipe(self, url):
        """
        Scrape a single recipe from TrueID Food website
        
        Args:
            url (str): Recipe URL or recipe ID
            
        Returns:
            dict: Recipe data with name, ingredients, steps
        """
        try:
            # Ensure full URL
            if url.startswith("http"):
                recipe_url = url
            else:
                recipe_url = f"{self.base_url}/detail/{url}"
            
            print(f"Scraping: {recipe_url[:60]}...")
            response = requests.get(recipe_url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract data
            name = self._get_recipe_name(soup)
            ingredients = self._get_ingredients(soup)
            steps = self._get_steps(soup)
            
            # Only return if we have valid data
            if name and ingredients:
                recipe_data = {
                    "name": name,
                    "ingredients": ingredients,
                    "steps": steps if steps else ["วิธีทำสามารถดูได้จากเว็บไซต์"],
                    "url": recipe_url,
                    "difficulty": self._get_difficulty(soup),
                    "time": self._get_time(soup),
                }
                return recipe_data
            else:
                print(f"⚠️  Missing data: name={name}, ingredients={len(ingredients)}")
                return None
                
        except Exception as e:
            print(f"❌ Error scraping {url}: {str(e)}")
            return None
    
    def _get_recipe_name(self, soup):
        """Extract recipe name from page"""
        try:
            h1 = soup.find("h1")
            if h1:
                name = h1.get_text(strip=True)
                if name and len(name) > 2:
                    return name
            return None
        except Exception as e:
            print(f"Error getting recipe name: {e}")
            return None
    
    def _get_ingredients(self, soup):
        """Extract ingredients from page"""
        try:
            ingredients = []
            
            # Common ingredient amount units (Thai cooking units)
            units = [
                "กรัม", "กก.", "ช้อน", "ช้อนโต๊ะ", "ช้อนชา",
                "ถ้วย", "ฟอง", "ชต.", "ชช.", "มล.", "ลิตร",
                "ซม.", "เซ็นติเมตร", "ขีด", "ชิ้น", "อย่าง", "ลูก",
                "หลอด", "แท่ง", "ห่อ", "กำ", "มัด", "ก้อน", "ซอย", "/",
            ]
            
            # Find all list items
            for li in soup.find_all("li"):
                text = li.get_text(strip=True)
                # Check if contains unit and reasonable length
                if any(unit in text for unit in units) and 5 < len(text) < 300:
                    if text not in ingredients and text.count(" ") < 20:
                        ingredients.append(text)
            
            return ingredients
            
        except Exception as e:
            print(f"Error getting ingredients: {e}")
            return []
    
    def _get_steps(self, soup):
        """Extract cooking steps from page"""
        try:
            steps = []
            
            # Look for numbered patterns in text
            # Match "1.", "2.", etc. followed by text
            for p in soup.find_all(["p", "li", "div"]):
                text = p.get_text(strip=True)
                
                # Check if starts with number pattern
                if re.match(r'^[\d]+\.\s+', text) and len(text) > 10:
                    if text not in steps:
                        steps.append(text)
            
            # Limit steps and filter out short ones
            steps = [s for s in steps if len(s) > 10][:20]
            
            return steps
            
        except Exception as e:
            print(f"Error getting steps: {e}")
            return []
    
    def _get_difficulty(self, soup):
        """Extract difficulty level"""
        try:
            page_text = soup.get_text().lower()
            
            if "ง่าย" in page_text or "easy" in page_text:
                return "ง่าย"
            elif "กลาง" in page_text or "medium" in page_text:
                return "กลาง"
            elif "ยาก" in page_text or "hard" in page_text:
                return "ยาก"
            
            return "ไม่ระบุ"
        except:
            return "ไม่ระบุ"
    
    def _get_time(self, soup):
        """Extract cooking time"""
        try:
            # Look for time patterns
            page_text = soup.get_text()
            time_pattern = r'(\d+)\s*นาที|(\d+)\s*min'
            match = re.search(time_pattern, page_text)
            if match:
                time_val = match.group(1) or match.group(2)
                return f"{time_val} นาที"
            return "ไม่ระบุ"
        except:
            return "ไม่ระบุ"
    
    def scrape_collection(self, collection_url, max_recipes=20):
        """
        Scrape all recipes from a collection page
        
        Args:
            collection_url (str): URL of collection/article page
            max_recipes (int): Maximum number of recipes to scrape
            
        Returns:
            list: List of recipe data dictionaries
        """
        print(f"\n📖 Extracting recipes from collection...")
        recipe_links = self.extract_recipe_links(collection_url)
        
        recipes = []
        for idx, link in enumerate(recipe_links[:max_recipes], 1):
            print(f"\n[{idx}/{min(len(recipe_links), max_recipes)}]", end=" ")
            recipe = self.scrape_recipe(link)
            if recipe:
                recipes.append(recipe)
            time.sleep(0.5)  # Be respectful with requests
        
        print(f"\n\n✅ Scraped {len(recipes)} recipes successfully")
        return recipes


def scrape_trueid_recipe(url):
    """
    Simple function to scrape a single TrueID recipe
    
    Args:
        url (str): Recipe URL or ID
        
    Returns:
        dict: Recipe data
    """
    scraper = TrueIDFoodScraper()
    return scraper.scrape_recipe(url)


def scrape_trueid_collection(url, max_recipes=20):
    """
    Scrape all recipes from a TrueID collection page
    
    Args:
        url (str): Collection URL
        max_recipes (int): Max recipes to scrape
        
    Returns:
        list: List of recipes
    """
    scraper = TrueIDFoodScraper()
    return scraper.scrape_collection(url, max_recipes)


if __name__ == "__main__":
    # Test the scraper
    scraper = TrueIDFoodScraper()
    
    print("="*70)
    print("TrueID Food Scraper Test")
    print("="*70)
    
    # Test 1: Single recipe
    print("\n[TEST 1] Scraping single recipe...")
    single_recipe = scraper.scrape_recipe("https://food.trueid.net/detail/mA1Jl95bpQgx")
    if single_recipe:
        print(f"✅ Recipe: {single_recipe['name']}")
        print(f"   Ingredients: {len(single_recipe['ingredients'])} items")
        print(f"   Steps: {len(single_recipe['steps'])} items")
    
    # Test 2: Collection page
    print("\n[TEST 2] Scraping collection page...")
    collection_recipes = scraper.scrape_collection(
        "https://food.trueid.net/detail/M6oyloE4klNB",
        max_recipes=3
    )
    if collection_recipes:
        print(f"\n✅ Successfully scraped {len(collection_recipes)} recipes")
        for recipe in collection_recipes:
            print(f"  - {recipe['name'][:60]}")
