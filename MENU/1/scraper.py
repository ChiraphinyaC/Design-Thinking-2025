import requests
from bs4 import BeautifulSoup
 
def scrape_kapook(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
 
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
 
    # ดึงชื่อสูตร
    title = soup.find("h1")
    recipe_name = title.get_text(strip=True) if title else "ไม่พบชื่อสูตร"
 
    # ดึงวัตถุดิบ (แบบกว้างก่อน เดี๋ยวปรับให้แม่นทีหลัง)
    ingredients = []
 
    for li in soup.find_all("li"):
        text = li.get_text(strip=True)
        if "กรัม" in text or "ช้อน" in text or "ถ้วย" in text or "ฟอง" in text:
            ingredients.append(text)
 
    return {
        "name": recipe_name,
        "ingredients": ingredients
    }