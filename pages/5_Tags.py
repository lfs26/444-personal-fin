import streamlit as st
from db import fetch_df, execute

st.title("🏷️ Tag Management")

# --- Add New Tag ---
tag_name = st.text_input("New Tag Name")
tag_color = st.color_picker("Tag Color", "#4CAF50")
tag_description = st.text_area("Description (optional)")


if st.button("Add Tag"):
    execute(
        "INSERT INTO tags (tag_name, tag_color) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
        (tag_name, tag_color)
    )
    st.success("Tag added!")

st.markdown("---")

# --- Existing Tags ---
df = fetch_df("SELECT * FROM tags ORDER BY tag_name;")
st.dataframe(df)
