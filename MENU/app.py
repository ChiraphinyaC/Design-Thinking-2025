import streamlit as st

st.set_page_config(page_title="เมนูวันนี้ จากวัตถุดิบที่มี", layout="wide")

# =========================
# 📦 DATA
# =========================
RECIPES = [
    {
        
        "id": 3,
        "name": "ต้มข่าไก่",
        "base_ingredients": 
        ["เนื้อไก่ (ส่วนที่ชอบ เช่น อกไก่ สะโพก น่องไก่ ฯลฯ)", "ข่า", "น้ำมะขามเปียก", "กะทิ",
        "ตะไคร้", "ใบมะกรูด", "หอมแดง", "พริกชี้ฟ้า","ผักชี", "เห็ดฟาง"],
        "protein_options": [],
        "images": {
            "default": "image/ต้มข่าไก่.jpg",
        },
        "type": "ต้ม",
        "difficulty": "ยาก",
        "time": "15–30",
        "steps": [
            "ต้มน้ำ ใส่ข่า ตะไคร้ ใบมะกรูด และพริก รอจนเดือดและหอม",
            "ใส่เนื้อไก่ลงไป ต้มจนเดือดอีกครั้ง",
            "ลดไฟลง ปรุงรสด้วยน้ำปลาและน้ำตาลทรายและน้ำมะขามเปียก ชิมรสตามชอบ",
            "ใส่กะทิลงไป ตามด้วยเห็ด ต้มจนเดือดแล้วปิดไฟ พร้อมเสิร์ฟ",
        ],
    },    
]

START_ING = [
    "หมู","ไก่","ไข่","เห็ดเข็มทอง","ผักกาด","ข้าว","เต้าหู้","กุ้ง","ปลา","วุ้นเส้น","มะนาว",
    "ตะไคร้","ขิง","ตับไก่","ตับหมู","กะทิ","มะเขือเทศ","มะเขือเปราะ","กระเพรา","พริก","กระเทียม",
    "โหรพา","หอมหัวใหญ่","แครอท","ถั่วฝักยาว","หอมแดง","ใบมะกรูด","พริกแห้ง","ผักคะน้า","ผักบุ้ง",
    "แตงกวา","กระชาย","ฟักทอง","มันฝรั่ง","มะเขือยาว","สะตอ","ผักหวาน","กระเจี๊ยบเขียว",
    "พริกหวาน","นมจืด","พริกหยวก","พริกหนุ่ม"
]

# =========================
# 🧠 SESSION STATE
# =========================
if "ingredients" not in st.session_state:
    st.session_state.ingredients = set(START_ING)

if "selected" not in st.session_state:
    st.session_state.selected = set()

if "filters" not in st.session_state:
    st.session_state.filters = {"type": "", "difficulty": "", "time": ""}

if "name_query" not in st.session_state:
    st.session_state.name_query = ""

# =========================
# 🖼 IMAGE HELPER
# =========================
def get_recipe_image(recipe):
    selected = st.session_state.selected
    for protein in recipe.get("protein_options", []):
        if protein in selected:
            return recipe["images"].get(protein, recipe["images"]["default"])
    return recipe["images"]["default"]

# =========================
# 🎯 MATCH LOGIC
# =========================
def matches(recipe):
    f = st.session_state.filters
    selected = st.session_state.selected

    if f["type"] and recipe["type"] != f["type"]:
        return False
    if f["difficulty"] and recipe["difficulty"] != f["difficulty"]:
        return False
    if f["time"] and recipe["time"] != f["time"]:
        return False

    if st.session_state.name_query:
        q = st.session_state.name_query
        searchable = (
            [recipe["name"]]
            + recipe.get("base_ingredients", [])
            + recipe.get("protein_options", [])
        )
        if not any(q in s.lower() for s in searchable):
            return False

    selected_base = [
        s for s in selected if s not in recipe.get("protein_options", [])
    ]
    selected_protein = [
        s for s in selected if s in recipe.get("protein_options", [])
    ]

    base_match = all(
        any(sb.lower() == ing.lower() for ing in recipe["base_ingredients"])
        for sb in selected_base
    )

    if recipe.get("protein_options"):
        protein_match = (
            True if not selected_protein
            else any(p in recipe["protein_options"] for p in selected_protein)
        )
    else:
        protein_match = True

    return base_match and protein_match

# =========================
# ⭐ MATCH SCORE
# =========================
def match_score(recipe):
    selected = st.session_state.selected
    if not selected:
        return 0

    all_ings = (
        recipe.get("base_ingredients", [])
        + recipe.get("protein_options", [])
    )

    match_count = sum(
        1 for sel in selected
        if any(sel.lower() == ing.lower() for ing in all_ings)
    )

    return match_count / len(selected)

# =========================
# 🎨 UI
# =========================
st.title("🍽️ เมนูวันนี้ จากวัตถุดิบที่มี")

search_val = st.text_input("พิมพ์ชื่อเมนูหรือวัตถุดิบ")
if search_val:
    st.session_state.name_query = search_val.lower()

col_sidebar, col_main = st.columns([1, 3])

# =========================
# 🧺 SIDEBAR
# =========================
with col_sidebar:
    st.subheader("วัตถุดิบ")

    sorted_ings = sorted(list(st.session_state.ingredients))
    selected_ings = st.multiselect(
        "เลือกวัตถุดิบ",
        sorted_ings,
        default=list(st.session_state.selected),
        label_visibility="collapsed",
    )
    st.session_state.selected = set(selected_ings)

    st.divider()
    st.subheader("ตัวกรอง")

    st.session_state.filters["type"] = st.selectbox(
        "ประเภทอาหาร", ["", "ต้ม", "ผัด", "แกง", "ทอด", "ยำ", "นึ่ง"]
    )

    col_diff, col_time = st.columns(2)

    with col_diff:
        st.session_state.filters["difficulty"] = st.selectbox(
            "ระดับความยาก", ["", "ง่าย", "กลาง", "ยาก"]
        )

    with col_time:
        st.session_state.filters["time"] = st.selectbox(
            "เวลา", ["", "<15", "15–30", ">30"]
        )

# =========================
# 🍽 MAIN
# =========================
with col_main:
    filtered = [r for r in RECIPES if matches(r)]
    results = sorted(filtered, key=lambda r: match_score(r), reverse=True)

    st.subheader(f"ผลลัพธ์สูตร ({len(results)} รายการ)")

    if not results:
        st.info("ไม่พบสูตรที่ตรงกับเงื่อนไข")

    cols = st.columns(3)
    for idx, recipe in enumerate(results):
        with cols[idx % 3]:
            with st.container(border=True):
                st.image(get_recipe_image(recipe), width="stretch")
                st.subheader(recipe["name"])
                st.caption(f"{recipe['type']} · {recipe['time']}")

                # 📖 วิธีทำ
                with st.expander("📖 วิธีทำ"):
                    for i, step in enumerate(recipe.get("steps", []), start=1):
                        st.write(f"{i}. {step}")

                score = match_score(recipe)
                if st.session_state.selected:
                    st.progress(score)
                    st.caption(f"ตรงวัตถุดิบ {score*100:.0f}%")
