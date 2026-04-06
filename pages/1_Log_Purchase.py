import streamlit as st
from db import fetch_df, execute

st.title("🛒 Log a Purchase")

categories = fetch_df("SELECT * FROM categories ORDER BY name;")

item = st.text_input("Item Purchased")
amount = st.number_input("Amount ($)", min_value=0.0)
category = st.selectbox("Category", categories["name"])
notes = st.text_area("Notes (optional)")

if st.button("Save Purchase"):
    cat_id = int(categories.loc[categories["name"] == category, "category_id"].iloc[0])
    execute(
        "INSERT INTO purchases (item, amount, category_id, notes) VALUES (%s, %s, %s, %s);",
        (item, amount, cat_id, notes)
    )
    st.success("Purchase logged!")
