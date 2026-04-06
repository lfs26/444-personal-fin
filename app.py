import streamlit as st
from db import fetch_df

st.set_page_config(page_title="Personal Finance Tracker", page_icon="💰", layout="wide")

st.title("💰 Personal Finance Tracker")
st.write("Track purchases, recurring bills, and spending trends.")

st.markdown("---")
st.subheader("📊 Overview")

try:
    purchases = fetch_df("SELECT COUNT(*) AS c FROM purchases;")
    bills = fetch_df("SELECT COUNT(*) AS c FROM recurring_bills;")
    total_spent = fetch_df("SELECT COALESCE(SUM(amount),0) AS s FROM purchases;")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Purchases", int(purchases["c"][0]))
    col2.metric("Recurring Bills", int(bills["c"][0]))
    col3.metric("Total Spent", f"${total_spent['s'][0]:,.2f}")

except Exception as e:
    st.error(f"Database error: {e}")
