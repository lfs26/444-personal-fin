import streamlit as st
from db import fetch_df, execute

st.title("🛒 Log a Purchase")

# -------------------------
# Load categories
# -------------------------
categories = fetch_df("SELECT * FROM categories ORDER BY name;")

item = st.text_input("Item Purchased")
amount = st.number_input("Amount ($)", min_value=0.0)
category = st.selectbox("Category", categories["name"])
notes = st.text_area("Notes (optional)")

# -------------------------
# Load tags BEFORE button
# -------------------------
tag_df = fetch_df("SELECT tag_id, tag_name FROM tags ORDER BY tag_name;")
tag_options = {row["tag_name"]: row["tag_id"] for _, row in tag_df.iterrows()}
selected_tags = st.multiselect("Tags", list(tag_options.keys()))

# -------------------------
# Save Purchase + Tags
# -------------------------
from db import fetch_df, execute, execute_returning   # ← add execute_returning

if st.button("Save Purchase"):
    cat_id = int(categories.loc[categories["name"] == category, "category_id"].iloc[0])

    # Use execute_returning instead of fetch_df for INSERT...RETURNING
    purchase_id = execute_returning("""
        INSERT INTO purchases (item, amount, category_id, notes)
        VALUES (%s, %s, %s, %s)
        RETURNING purchase_id;
    """, (item, amount, cat_id, notes))

    if selected_tags:
        for tag_name in selected_tags:
            tag_id = tag_options.get(tag_name)
            if tag_id is None:
                continue
            execute(
                "INSERT INTO purchase_tags (purchase_id, tag_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
                (int(purchase_id), int(tag_id))   # ← explicit int() as a safety net
            )

    st.success("Purchase logged!")

