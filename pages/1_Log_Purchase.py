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
# Load tags
tag_df = fetch_df("SELECT tag_id, tag_name FROM tags ORDER BY tag_name;")
tag_options = {row["tag_name"]: row["tag_id"] for _, row in tag_df.iterrows()}

selected_tags = st.multiselect("Tags", list(tag_options.keys()))

purchase_id = fetch_df("SELECT MAX(purchase_id) AS id FROM purchases;")["id"].iloc[0]

for tag_name in selected_tags:
    tag_id = tag_options[tag_name]
    execute(
        "INSERT INTO purchase_tags (purchase_id, tag_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
        (purchase_id, tag_id)
    )
