import streamlit as st
from db import fetch_df, execute

st.title("🗂 Manage Purchases")

df = fetch_df("""
    SELECT p.purchase_id, p.item, p.amount, c.name AS category, p.purchase_date
    FROM purchases p
    JOIN categories c ON p.category_id = c.category_id
    ORDER BY p.purchase_date DESC;
""")

st.subheader("Edit Selected Purchase")

edit_item = st.text_input("Item", selected_row["item"])
edit_amount = st.number_input("Amount ($)", min_value=0.0, value=float(selected_row["amount"]))
edit_notes = st.text_area("Notes", selected_row["notes"])

if st.button("Save Changes"):
    execute("""
        UPDATE purchases
        SET item = %s, amount = %s, notes = %s
        WHERE purchase_id = %s;
    """, (edit_item, edit_amount, edit_notes, selected_purchase_id))

    st.success("Purchase updated successfully.")

st.dataframe(df, use_container_width=True)

ids = df["purchase_id"].tolist()
selected = st.selectbox("Select purchase to delete", ids)

if st.button("Delete Purchase"):
    st.warning("Are you sure you want to delete this record? This action cannot be undone.")
    confirm = st.button("Yes, delete permanently")
    if confirm:
        execute("DELETE FROM purchases WHERE purchase_id = %s;", (purchase_id,))
        st.success("Record deleted.")

