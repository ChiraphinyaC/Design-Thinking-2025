import streamlit as st
import pandas as pd
from typing import Set, List

st.set_page_config(page_title="เมนูวันนี้ จากวัตถุดิบที่มี", layout="wide")

# Recipe data
RECIPES = [
    {
        "id": 1,
        "name": "ผัดกระเพราไก่",
        "image": "https://source.unsplash.com/400x300/?stirfry",
        "labels": ["เผ็ด"],
        "ingredients": ["ไก่", "กระเพรา", "พริก"],
        "type": "ผัด",
        "diet": "ไม่ใส่เนื้อ",
        "difficulty": "ง่าย",
        "time": "15–30",
        "popularity": 8,
        "recipe_url": "",
    },
    {
        "id": 2,
        "name": "ต้มยำกุ้ง",
        "image": "https://source.unsplash.com/400x300/?soup",
        "labels": ["เผ็ด"],
        "ingredients": ["กุ้ง", "ตะไคร้", "มะนาว"],
        "type": "ต้ม",
        "diet": "ไม่ใส่เนื้อ",
        "difficulty": "กลาง",
        "time": "15–30",
        "popularity": 10,
        "recipe_url": "",
    },
    {
        "id": 3,
        "name": "แกงเขียวหวานเจ",
        "image": "https://source.unsplash.com/400x300/?curry",
        "labels": ["เจ"],
        "ingredients": ["มะเขือ", "มะเขือเทศ", "กะทิ"],
        "type": "แกง",
        "diet": "เจ",
        "difficulty": "กลาง",
        "time": ">30",
        "popularity": 6,
        "recipe_url": "",
    },
    {
        "id": 4,
        "name": "สลัดผักรวม",
        "image": "https://source.unsplash.com/400x300/?salad",
        "labels": ["ง่าย"],
        "ingredients": ["ผัก", "มะเขือเทศ", "น้ำสลัด"],
        "type": "ยำ",
        "diet": "มังสวิรัติ",
        "difficulty": "ง่าย",
        "time": "<15",
        "popularity": 7,
        "recipe_url": "",
    },
    {
        "id": 5,
        "name": "ปลาทอดกระเทียม",
        "image": "https://source.unsplash.com/400x300/?fried",
        "labels": ["ไม่ใส่เนื้อ"],
        "ingredients": ["ปลา", "กระเทียม", "น้ำปลา"],
        "type": "ทอด",
        "diet": "ไม่ใส่เนื้อ",
        "difficulty": "กลาง",
        "time": "15–30",
        "popularity": 5,
        "recipe_url": "",
    },
]

START_ING = ["หมู", "ไก่", "ไข่", "เห็ด", "ผัก", "ข้าว", "เต้าหู้", "กุ้ง", "ปลา"]

# Initialize session state
if "ingredients" not in st.session_state:
    st.session_state.ingredients = set(START_ING)
if "selected" not in st.session_state:
    st.session_state.selected = set()
if "filters" not in st.session_state:
    st.session_state.filters = {"type": "", "diet": "", "difficulty": "", "time": ""}
if "name_query" not in st.session_state:
    st.session_state.name_query = ""

# Header
st.title("🍽️ เมนูวันนี้ จากวัตถุดิบที่มี")

col1, col2 = st.columns([3, 1])
with col1:
    search_val = st.text_input("พิมพ์ชื่อเมนูหรือวัตถุดิบ", key="search_input")
with col2:
    if st.button("ค้นหา"):
        if search_val.strip():
            st.session_state.name_query = search_val.lower()
            # Check if ingredient exists
            match = next(
                (i for i in st.session_state.ingredients if i.lower() == search_val.lower()),
                None,
            )
            if match:
                st.session_state.selected.add(match)
            else:
                st.session_state.ingredients.add(search_val.strip())
                st.session_state.selected.add(search_val.strip())
            st.rerun()

# Main layout
col_sidebar, col_main = st.columns([1, 3])

with col_sidebar:
    st.subheader("วัตถุดิบ")

    # Display ingredients
    sorted_ings = sorted(list(st.session_state.ingredients))
    selected_ings = st.multiselect(
        "เลือกวัตถุดิบ",
        sorted_ings,
        default=list(st.session_state.selected),
        label_visibility="collapsed",
    )
    st.session_state.selected = set(selected_ings)

    # Add new ingredient
    new_ing = st.text_input("เพิ่มวัตถุดิบอื่น ๆ")
    if new_ing:
        if new_ing.strip() and new_ing.strip() not in st.session_state.ingredients:
            st.session_state.ingredients.add(new_ing.strip())
            st.rerun()

    st.divider()

    # Filters
    st.subheader("ตัวกรอง")

    filter_type = st.selectbox(
        "ประเภทอาหาร",
        ["", "ต้ม", "ผัด", "แกง", "ทอด", "ยำ", "นึ่ง"],
        index=0,
    )
    st.session_state.filters["type"] = filter_type

    filter_diet = st.selectbox(
        "ข้อจำกัดอาหาร",
        ["", "เจ", "มังสวิรัติ", "ฮาลาล", "ไม่ใส่เนื้อ"],
        index=0,
    )
    st.session_state.filters["diet"] = filter_diet

    col_diff, col_time = st.columns(2)
    with col_diff:
        filter_diff = st.selectbox(
            "ระดับความยาก", ["", "ง่าย", "กลาง", "ยาก"], index=0
        )
        st.session_state.filters["difficulty"] = filter_diff

    with col_time:
        filter_time = st.selectbox(
            "เวลา", ["", "<15", "15–30", ">30"], index=0
        )
        st.session_state.filters["time"] = filter_time

with col_main:
    # Filter recipes
    def matches(recipe):
        f = st.session_state.filters
        if f["type"] and recipe["type"] != f["type"]:
            return False
        if f["diet"] and recipe["diet"] != f["diet"]:
            return False
        if f["difficulty"] and recipe["difficulty"] != f["difficulty"]:
            return False
        if f["time"] and recipe["time"] != f["time"]:
            return False

        if st.session_state.name_query:
            q = st.session_state.name_query
            if (
                q not in recipe["name"].lower()
                and not any(q in ing.lower() for ing in recipe["ingredients"])
            ):
                return False

        for sel in st.session_state.selected:
            if not any(
                sel.lower() == ing.lower() for ing in recipe["ingredients"]
            ):
                return False

        return True

    results = [r for r in RECIPES if matches(r)]

    # Display results
    st.subheader(f"ผลลัพธ์สูตร ({len(results)} รายการ)")

    if len(results) == 0:
        st.info("ไม่พบสูตรที่ตรงกับเงื่อนไข")
    else:
        # Display recipe cards
        cols = st.columns(3)
        for idx, recipe in enumerate(results):
            with cols[idx % 3]:
                with st.container(border=True):
                    st.image(recipe["image"], use_column_width=True)
                    st.subheader(recipe["name"])
                    st.caption(f"{recipe['type']} · {recipe['time']}")

                    # Labels
                    label_text = " ".join(
                        [f"`{label}`" for label in recipe["labels"]]
                    )
                    if label_text:
                        st.markdown(label_text)

                    if st.button("ดูสูตร", key=f"recipe_{recipe['id']}"):
                        st.session_state[f"show_recipe_{recipe['id']}"] = True

                    # Show recipe details in expander
                    if st.session_state.get(f"show_recipe_{recipe['id']}", False):
                        with st.expander("รายละเอียดสูตร", expanded=True):
                            st.write(f"**ประเภท:** {recipe['type']}")
                            st.write(f"**เวลา:** {recipe['time']}")
                            st.write(f"**ข้อจำกัด:** {recipe['diet']}")
                            st.write(f"**ความยาก:** {recipe['difficulty']}")
                            st.write(f"**วัตถุดิบ:** {', '.join(recipe['ingredients'])}")
                            if recipe["recipe_url"]:
                                st.markdown(
                                    f"[ดูสูตรที่มา]({recipe['recipe_url']})"
                                )
                            else:
                                st.info("สูตรอาหารจะเพิ่มในภายหลัง")

    # Recommended section
    if len(results) > 0:
        pool = results
    else:
        pool = RECIPES

    sorted_recommended = sorted(pool, key=lambda x: x["popularity"], reverse=True)[
        :6
    ]

    if sorted_recommended:
        st.divider()
        st.subheader("✨ สูตรยอดนิยม")
        rec_cols = st.columns(len(sorted_recommended))
        for col, recipe in zip(rec_cols, sorted_recommended):
            with col:
                with st.container(border=True):
                    st.image(recipe["image"], use_column_width=True)
                    st.caption(recipe["name"])
                    st.caption(f"{recipe['type']} · {recipe['time']}")
