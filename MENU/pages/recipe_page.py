import streamlit as st

st.set_page_config(page_title="รายละเอียดสูตร", layout="wide")

if "selected_recipe" not in st.session_state:
    st.warning("ไม่พบสูตรที่เลือก")
    st.stop()

recipe = st.session_state.selected_recipe

st.title(recipe["name"])

st.image(recipe["image"], use_column_width=True)

st.subheader("ข้อมูลทั่วไป")
st.write(f"ประเภท: {recipe['type']}")
st.write(f"เวลา: {recipe['time']}")
st.write(f"ข้อจำกัด: {recipe['diet']}")
st.write(f"ระดับความยาก: {recipe['difficulty']}")

st.subheader("วัตถุดิบ")
for ing in recipe["ingredients"]:
    st.write("•", ing)

if st.button("⬅ กลับหน้าหลัก"):
    st.switch_page("app.py")
