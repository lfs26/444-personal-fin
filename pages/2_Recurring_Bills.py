import streamlit as st
from db import fetch_df, execute
import re

st.title("📆 Recurring Bills")

# -------------------------
# Add New Bill
# -------------------------
name = st.text_input("Bill Name")
amount = st.number_input("Amount ($)", min_value=0.0)
due_day = st.number_input("Due Day (1–31)", min_value=1, max_value=31)
frequency = st.selectbox("Frequency", ["monthly", "weekly", "yearly"])
billing_email = st.text_input("Billing Email (used to pay this bill)")
notes = st.text_area("Notes (optional)")

email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

if st.button("Add Bill"):

    # --- Validation ---
    if not name:
        st.error("Bill name is required.")
    elif amount <= 0:
        st.error("Amount must be greater than zero.")
    elif billing_email and not re.match(email_pattern, billing_email):
        st.error("Please enter a valid email address.")
    else:
        execute(
            """
            INSERT INTO recurring_bills (name, amount, due_day, frequency, notes, billing_email)
            VALUES (%s, %s, %s, %s, %s, %s);
            """,
            (name, amount, due_day, frequency, notes, billing_email)
        )
        st.success("Recurring bill added!")

st.markdown("---")
st.subheader("Existing Bills")

# -------------------------
# Load Bills
# -------------------------
df = fetch_df("SELECT * FROM recurring_bills ORDER BY due_day;")

df["name"] = df["name"].astype(str).str.strip()

bill_list = df["name"].tolist()
selected_bill = st.selectbox("Select bill to log as a purchase", bill_list)

# -------------------------
# Get Bills category_id
# -------------------------
cat = fetch_df("SELECT category_id FROM categories WHERE name = 'Bills';")
bills_cat_id = int(cat["category_id"].iloc[0])

# -------------------------
# Log Bill Payment
# -------------------------
if st.button("Log Bill Payment"):
    row = df[df["name"] == selected_bill].iloc[0]

    item = str(row["name"])
    amount = float(row["amount"])
    category_id = bills_cat_id
    notes = "Auto-logged from recurring bills"

    execute(
        """
        INSERT INTO purchases (item, amount, category_id, notes)
        VALUES (%s, %s, %s, %s);
        """,
        (item, amount, category_id, notes)
    )

    st.success("Bill logged as a purchase!")
