import streamlit as st
from db import fetch_df

st.title("📈 Spending Summary")
tag_df = fetch_df("SELECT tag_id, tag_name FROM tags ORDER BY tag_name;")
tag_options = {row["tag_name"]: row["tag_id"] for _, row in tag_df.iterrows()}

selected_tag = st.selectbox("Filter by Tag", ["All"] + list(tag_options.keys()))
if selected_tag == "All":
    purchases_df = fetch_df("SELECT * FROM purchases ORDER BY purchase_date DESC;")
else:
    tag_id = tag_options[selected_tag]
    purchases_df = fetch_df("""
        SELECT p.*
        FROM purchases p
        JOIN purchase_tags pt ON p.purchase_id = pt.purchase_id
        WHERE pt.tag_id = %s
        ORDER BY p.purchase_date DESC;
    """, (tag_id,))


summary_df = fetch_df("""
    SELECT c.name AS category, SUM(p.amount) AS total
    FROM purchases p
    JOIN categories c ON p.category_id = c.category_id
    GROUP BY c.name
    ORDER BY total DESC;
""")

st.bar_chart(summary_df.set_index("category"))
st.dataframe(summary_df, use_container_width=True)

bills = fetch_df("""
    SELECT name AS category, SUM(amount) AS total
    FROM recurring_bills
    GROUP BY name;
""")

st.subheader("📆 Monthly Bill Obligations")
st.dataframe(bills, use_container_width=True)

# --- All Purchases Section ---
st.subheader("🧾 All Purchases" if selected_tag == "All" else f"🧾 Purchases tagged: {selected_tag}")

if selected_tag == "All":
    purchases_df = fetch_df("""
        SELECT p.purchase_date, p.description, p.amount,
               STRING_AGG(t.tag_name, ', ') AS tags
        FROM purchases p
        LEFT JOIN purchase_tags pt ON p.purchase_id = pt.purchase_id
        LEFT JOIN tags t ON pt.tag_id = t.tag_id
        GROUP BY p.purchase_id, p.purchase_date, p.description, p.amount
        ORDER BY p.purchase_date DESC;
    """)
else:
    purchases_df = fetch_df("""
        SELECT p.purchase_date, p.description, p.amount,
           GROUP_CONCAT(t.tag_name, ', ') AS tags
        FROM purchases p
        LEFT JOIN purchase_tags pt ON p.purchase_id = pt.purchase_id
        LEFT JOIN tags t ON pt.tag_id = t.tag_id
        WHERE p.purchase_id IN (
            SELECT purchase_id FROM purchase_tags
            WHERE tag_id = %s
        )
        GROUP BY p.purchase_id, p.purchase_date, p.description, p.amount
        ORDER BY p.purchase_date DESC;
    """, (tag_id,))

st.dataframe(purchases_df, use_container_width=True)
