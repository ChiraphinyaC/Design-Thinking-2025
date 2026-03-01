#scrape_runner.py : ตัว “รันเก็บข้อมูลจำนวนมาก”
#หน้าที่ ดึงหลายสูตรจาก Kapook วนลูปหลาย URL บันทึก CSV สร้าง dataset
import pandas as pd
from scraper import scrape_kapook
import time

# 🔥 ใส่ลิงก์สูตรที่ต้องการ
URLS = [
    "https://cooking.kapook.com/view273026.html",
]


def main():
    all_rows = []

    for url in URLS:
        print("กำลังดึง:", url)
        data = scrape_kapook(url)

        if not data:
            continue

        all_rows.append({
            "recipe_name": data["name"],
            "ingredients": "|".join(data["ingredients"]),
            "steps": "|".join(data["steps"]),
            "type": "",
            "difficulty": "",
            "time": "",
            "image": data["image"],
        })

        time.sleep(1)

    df = pd.DataFrame(all_rows)
    df.to_csv("recipes_dataset.csv", index=False, encoding="utf-8-sig")

    print("✅ สร้าง recipes_dataset.csv สำเร็จ")


if __name__ == "__main__":
    main()
