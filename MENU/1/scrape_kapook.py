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
    response = requests.get(list_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
 
    links = []
 
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "cooking.kapook.com/view" in href:
            if href.startswith("http"):
                links.append(href)
            else:
                links.append("https://cooking.kapook.com" + href)
 
    # ลบลิงก์ซ้ำ
    links = list(set(links))
 
    return links
 
 
# ----------------------------------
# ดึงรายละเอียดสูตร
# ----------------------------------
def scrape_kapook(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
 
    title_tag = soup.find("h1")
    recipe_name = title_tag.get_text(strip=True) if title_tag else "ไม่พบชื่อสูตร"
 
    ingredients = []
    for li in soup.find_all("li"):
        text = li.get_text(strip=True)
        if any(unit in text for unit in ["กรัม", "ช้อน", "ถ้วย", "ฟอง", "ชต.", "ชช.", "มล."]):
            ingredients.append(text)
 
    steps = []
    for p in soup.find_all("p"):
        text = p.get_text(strip=True)
        if text.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")):
            steps.append(text)
    steps = list(dict.fromkeys(steps))
    return {
        "recipe_name": recipe_name,
        "ingredients": ingredients,
        "steps": steps
    }
 
 
# ----------------------------------
# 🔥 รันหลัก
# ----------------------------------
if __name__ == "__main__":
 
    list_page = "https://cooking.kapook.com/"
 
    print("กำลังดึงลิงก์สูตร...")
    recipe_links = get_recipe_links(list_page)
 
    print("พบลิงก์ทั้งหมด:", len(recipe_links))
 
    all_data = []
 
    # จำกัดจำนวนก่อนเพื่อทดสอบ (เช่น 10 สูตรแรก)
    for url in recipe_links[:10]:
        print("กำลังดึง:", url)
 
        data = scrape_kapook(url)
 
        if data and len(data["ingredients"]) > 0:
            all_data.append({
                "recipe_name": data["recipe_name"],
                "ingredients_text": " | ".join(data["ingredients"]),
                "steps_text": " | ".join(data["steps"])
            })
 
        time.sleep(1)  # หน่วงเวลา ป้องกันโดนบล็อก
 
    df = pd.DataFrame(all_data)
    df.to_csv("recipes_dataset.csv", index=False, encoding="utf-8-sig")
 
    print("บันทึกไฟล์ recipes_dataset.csv สำเร็จ")
 