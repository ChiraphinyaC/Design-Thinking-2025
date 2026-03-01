import requests
from bs4 import BeautifulSoup


def scrape_kapook(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # -------------------
        #  ชื่อสูตร
        # -------------------
        title = soup.find("h1")
        recipe_name = title.get_text(strip=True) if title else "ไม่พบชื่อสูตร"

        # -------------------
        #  วัตถุดิบ
        # -------------------
        units = [
            "กรัม", "กก.", "ช้อน", "ช้อนโต๊ะ", "ช้อนชา",
            "ถ้วย", "ฟอง", "ชต.", "ชช.", "มล.", "ลิตร"
        ]

        ingredients = []

        for li in soup.find_all("li"):
            text = li.get_text(strip=True)

            if any(unit in text for unit in units):
                if 2 < len(text) < 200:  # กันข้อความเพี้ยน
                    ingredients.append(text)

        # ลบซ้ำแต่รักษาลำดับ
        ingredients = list(dict.fromkeys(ingredients))

        return {
            "name": recipe_name,
            "ingredients": ingredients
        }
