import streamlit as st
from db import fetch_df, execute

st.title("📆 Recurring Bills")

name = st.text_input("Bill Name")
amount = st.number_input("Amount ($)", min_value=0.0)
due_day = st.number_input("Due Day (1–31)", min_value=1, max_value=31)
frequency = st.selectbox("Frequency", ["monthly", "weekly", "yearly"])
notes = st.text_area("Notes (optional)")

if st.button("Add Bill"):
    execute(
        "INSERT INTO recurring_bills (name, amount, due_day, frequency, notes) VALUES (%s, %s, %s, %s, %s);",
        (name, amount, due_day, frequency, notes)
    )
    st.success("Recurring bill added!")

st.markdown("---")
st.subheader("Existing Bills")

df = fetch_df("SELECT * FROM recurring_bills ORDER BY bill_id;")

st.write("DEBUG COLUMNS:", df.columns.tolist())
st.dataframe(df)

st.dataframe(df, use_container_width=True)


if st.button("Log Bill Payment"):
    row = df[df["name"] == selected_bill].iloc[0]

    # Get category_id for "Bills"
    cat = fetch_df("SELECT category_id FROM categories WHERE name = 'Bills';")
    bills_cat_id = int(cat["category_id"].iloc[0])

    # Convert numpy → Python native types
    item = str(row["name"])
    amount = float(row["amount"])
    category_id = int(bills_cat_id)
    notes = "Auto-logged from recurring bills"

    execute("""
        INSERT INTO purchases (item, amount, category_id, notes)
        VALUES (%s, %s, %s, %s);
    """, (item, amount, category_id, notes))

    st.success("Bill logged as a purchase!")
