import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

# ----------------------------------
# ดึงลิงก์สูตรจากหน้ารวม
# ----------------------------------
def get_recipe_links(list_url):
    try:
        response = requests.get(list_url, headers=headers, timeout=10)
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


# ----------------------------------
# ดึงรายละเอียดสูตร
# ----------------------------------
def scrape_kapook(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        #  title
        title_tag = soup.find("h1")
        recipe_name = title_tag.get_text(strip=True) if title_tag else "ไม่พบชื่อสูตร"

        #  ingredients (แม่นขึ้น)
        ingredients = []
        for li in soup.select("li"):
            text = li.get_text(strip=True)

            if any(unit in text for unit in
                   ["กรัม", "ช้อน", "ถ้วย", "ฟอง", "ชต.", "ชช.", "มล."]):
                if len(text) < 200:  # กันข้อความยาวผิดปกติ
                    ingredients.append(text)

        #  steps (ยืดหยุ่นขึ้น)
        steps = []
        for p in soup.find_all("p"):
            text = p.get_text(strip=True)

            if (
                text.startswith(tuple(str(i) for i in range(1, 10))) or
                "ขั้นตอน" in text
            ):
                steps.append(text)

        steps = list(dict.fromkeys(steps))

        return {
            "recipe_name": recipe_name,
            "ingredients": ingredients,
            "steps": steps
        }

    except Exception as e:
        print(f"❌ scrape error {url}:", e)
        return None


# ----------------------------------
#  main
# ----------------------------------
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
                "recipe_name": data["recipe_name"],
                "ingredients_text": " | ".join(data["ingredients"]),
                "steps_text": " | ".join(data["steps"])
            })

        time.sleep(1)

    df = pd.DataFrame(all_data)
    df.to_csv("recipes_dataset.csv", index=False, encoding="utf-8-sig")

    print("✅ บันทึกไฟล์ recipes_dataset.csv สำเร็จ")
