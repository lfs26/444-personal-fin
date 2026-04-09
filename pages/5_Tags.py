import streamlit as st
from db import fetch_df, execute

st.title("🏷️ Tag Management")

# -------------------------
# Add New Tag
# -------------------------
st.subheader("Add a New Tag")

tag_name = st.text_input("Tag Name")
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
    st.success("Tag added or updated!")


st.markdown("---")

# -------------------------
# View Existing Tags
# -------------------------
st.subheader("Existing Tags")

df = fetch_df("SELECT * FROM tags ORDER BY tag_name;")
st.dataframe(df)


st.markdown("---")

# -------------------------
# Delete Tag
# -------------------------
st.subheader("Delete a Tag")

# Load tags for deletion
delete_options = {row["tag_name"]: row["tag_id"] for _, row in df.iterrows()}

tag_to_delete = st.selectbox("Select a tag to delete", ["None"] + list(delete_options.keys()))

if tag_to_delete != "None":
    if st.button("Delete Selected Tag"):
        tag_id = delete_options[tag_to_delete]

        # First delete from purchase_tags to avoid FK errors
        execute("DELETE FROM purchase_tags WHERE tag_id = %s;", (tag_id,))

        # Then delete the tag itself
        execute("DELETE FROM tags WHERE tag_id = %s;", (tag_id,))

        st.success(f"Tag '{tag_to_delete}' deleted!")
