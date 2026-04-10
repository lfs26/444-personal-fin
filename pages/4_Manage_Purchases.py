import streamlit as st
from db import fetch_df, execute

st.title("🧾 Manage Purchases")

# -------------------------
# Load Purchases
# -------------------------
purchases = fetch_df("""
SELECT p.purchase_id,
       p.item,
       p.amount,
       c.name AS category,
       p.notes
FROM purchases p
LEFT JOIN categories c ON p.category_id = c.category_id
ORDER BY p.purchase_id DESC;
""")

# If no purchases exist, stop the page safely
if purchases.empty:
    st.info("No purchases found.")
    st.stop()

st.dataframe(purchases, use_container_width=True)

# -------------------------
# Select Purchase
# -------------------------
purchase_ids = purchases["purchase_id"].tolist()
selected_id = st.selectbox("Select a purchase to edit", purchase_ids)

# -------------------------
# Safely get selected row
# -------------------------
selected_row = purchases[purchases["purchase_id"] == selected_id].iloc[0]

st.markdown("---")
st.subheader("✏️ Edit Purchase")

# -------------------------
# Edit Fields
# -------------------------
edit_item = st.text_input("Item", selected_row["item"])
edit_amount = st.number_input("Amount ($)", min_value=0.0, value=float(selected_row["amount"]))
edit_notes = st.text_area("Notes", selected_row["notes"])

if st.button("Save Changes"):
    execute("""
        UPDATE purchases
        SET item = %s, amount = %s, notes = %s
        WHERE purchase_id = %s;
    """, (edit_item, edit_amount, edit_notes, selected_id))

    st.success("Purchase updated successfully.")

st.markdown("---")
st.subheader("🗑️ Delete Purchase")

if st.button("Delete Purchase"):
    st.warning("Are you sure you want to delete this purchase? This action cannot be undone.")

    if st.button("Yes, delete permanently"):
        execute("DELETE FROM purchases WHERE purchase_id = %s;", (selected_id,))
        st.success("Purchase deleted.")
        st.experimental_rerun()

