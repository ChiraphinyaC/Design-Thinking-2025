from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def recipe():
    data = {
        "title": "ต้มยำกุ้งน้ำใส",
        "description": "วัตถุดิบและส่วนผสมสำหรับสูตรอาหารไทยยอดนิยม",
        "ingredients_main": [
            {"icon": "🦐", "name": "กุ้ง", "qty": "250 กรัม", "desc": "กุ้งสดตัวใหญ่"},
            {"icon": "💧", "name": "น้ำสต็อก/น้ำซุป", "qty": "1 ลิตร", "desc": "น้ำสต็อกไก่หรือน้ำซุปปลา"},
            {"icon": "🌾", "name": "ตะไคร้", "qty": "3-4 ต้น", "desc": "คั่นให้ออกน้ำหอม"},
            {"icon": "🥒", "name": "ข่า", "qty": "3-4 ชิ้น", "desc": "หั่นบาง"},
        ],
        "seasoning": [
            {"icon": "🍋", "name": "น้ำมะนาว", "qty": "3 ช้อนโต๊ะ", "desc": "มะนาวสด"},
            {"icon": "🐟", "name": "น้ำปลา", "qty": "3 ช้อนโต๊ะ", "desc": "น้ำปลาคุณภาพดี"},
        ],
        "steps": [
            "เตรียมวัตถุดิบทั้งหมดให้พร้อม",
            "ต้มน้ำซุป ใส่ตะไคร้ ข่า และเครื่องสมุนไพร",
            "ใส่กุ้งและเห็ด ต้มจนกุ้งสุก",
            "ปรุงรสด้วยน้ำปลาและน้ำมะนาว",
        ]
    }

    return render_template("recipe.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
