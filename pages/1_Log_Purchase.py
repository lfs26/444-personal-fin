import streamlit as st
from db import fetch_df, execute

st.title("🛒 Log a Purchase")

# -------------------------
# Load categories
# -------------------------
categories = fetch_df("SELECT category_id, name FROM categories ORDER BY name;")

item = st.text_input("Item Purchased")
amount = st.number_input("Amount ($)", min_value=0.0, format="%.2f")
category_name = st.selectbox("Category", categories["name"])
notes = st.text_area("Notes (optional)")

# ⭐ NEW: Date field
purchase_date = st.date_input("Purchase Date")

# -------------------------
# Load tags BEFORE button
# -------------------------
tag_df = fetch_df("SELECT tag_id, tag_name FROM tags ORDER BY tag_name;")
tag_options = {row["tag_name"]: row["tag_id"] for _, row in tag_df.iterrows()}
selected_tags = st.multiselect("Tags", list(tag_options.keys()))

# -------------------------
# Save Purchase + Tags
# -------------------------
if st.button("Save Purchase"):

    if not item or amount <= 0:
        st.error("Please enter a valid item and amount.")
    else:
        # 1. Insert purchase and RETURN purchase_id
        cat_id = int(categories.loc[categories["name"] == category_name, "category_id"].iloc[0])

        purchase_id_df = fetch_df("""
            INSERT INTO purchases (item, amount, category_id, notes, purchased_at)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING purchase_id;
        """, (item, amount, cat_id, notes, purchase_date))

        purchase_id = int(purchase_id_df["purchase_id"].iloc[0])

        # 2. Insert tags ONLY if user selected tags
        if selected_tags:
            for tag_name in selected_tags:
                tag_id = tag_options.get(tag_name)
                if tag_id:
                    execute("""
                        INSERT INTO purchase_tags (purchase_id, tag_id)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING;
                    """, (purchase_id, tag_id))

        st.success("Purchase logged!")
