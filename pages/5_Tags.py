import streamlit as st
from db import fetch_df, execute

st.title("🏷️ Tag Management")

# --- Add New Tag ---
tag_name = st.text_input("New Tag Name")
tag_color = st.color_picker("Tag Color", "#4CAF50")
tag_description = st.text_area("Description (optional)")


if st.button("Add Tag"):
    execute(
    """
    INSERT INTO tags (tag_name, tag_color, description)
    VALUES (%s, %s, %s)
    ON CONFLICT (tag_name) DO UPDATE
        SET tag_color = EXCLUDED.tag_color,
            description = EXCLUDED.description;
    """,
    (tag_name, tag_color, tag_description)
)

    st.success("Tag added!")

st.markdown("---")

# --- Existing Tags ---
df = fetch_df("SELECT * FROM tags ORDER BY tag_name;")
st.dataframe(df)
