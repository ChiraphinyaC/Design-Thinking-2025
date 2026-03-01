#test_scrape.py : ตัวทดสอบสูตรเดียว
#หน้าที่ debug scraper เช็กว่า selector ยังใช้ได้ไหม
from scraper import scrape_kapook

url = "https://cooking.kapook.com/view273026.html"

data = scrape_kapook(url)

if data:
    print("ชื่อสูตร:", data["name"])
    print("วัตถุดิบ:")

    for ing in data["ingredients"]:
        print("-", ing)
else:
    print("❌ ดึงข้อมูลไม่สำเร็จ")
