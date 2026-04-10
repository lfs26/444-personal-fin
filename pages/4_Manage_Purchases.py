import streamlit as st
from db import fetch_df, execute

st.title("🗂 Manage Purchases")

df = fetch_df("""
    SELECT p.purchase_id, p.item, p.amount, c.name AS category, p.purchase_date
    FROM purchases p
    JOIN categories c ON p.category_id = c.category_id
    ORDER BY p.purchase_date DESC;
""")

st.dataframe(df, use_container_width=True)

ids = df["purchase_id"].tolist()
selected = st.selectbox("Select purchase to delete", ids)

if st.button("Delete Purchase"):
    st.warning("Are you sure you want to delete this record? This action cannot be undone.")
    confirm = st.button("Yes, delete permanently")
    if confirm:
        execute("DELETE FROM purchases WHERE purchase_id = %s;", (purchase_id,))
        st.success("Record deleted.")

