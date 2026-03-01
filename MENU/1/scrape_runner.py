import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from scraper import scrape_kapook


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_recipe_links(list_url):
    try:
        response = requests.get(list_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        links = set()

        for a in soup.select("a[href*='cooking.kapook.com/view']"):
            href = a["href"]

            if href.startswith("http"):
                links.add(href)
            else:
                links.add("https://cooking.kapook.com" + href)

        return list(links)

    except Exception as e:
        print("❌ get_recipe_links error:", e)
        return []


if __name__ == "__main__":

    list_page = "https://cooking.kapook.com/"

    print("กำลังดึงลิงก์สูตร...")
    recipe_links = get_recipe_links(list_page)

    print("พบลิงก์ทั้งหมด:", len(recipe_links))

    all_data = []

    for url in recipe_links[:10]:
        print("กำลังดึง:", url)

        data = scrape_kapook(url)

        if data and data["ingredients"]:
            all_data.append({
                "recipe_name": data["name"],
                "ingredients_text": " | ".join(data["ingredients"])
            })

        time.sleep(1)

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv("recipes_dataset.csv", index=False, encoding="utf-8-sig")
        print("✅ บันทึกไฟล์ recipes_dataset.csv สำเร็จ")
    else:
        print("❌ ไม่มีข้อมูลให้บันทึก")
