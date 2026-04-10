import streamlit as st
from db import fetch_df

st.title("📈 Spending Summary")
tag_df = fetch_df("SELECT tag_id, tag_name FROM tags ORDER BY tag_name;")
tag_options = {row["tag_name"]: row["tag_id"] for _, row in tag_df.iterrows()}

selected_tag = st.selectbox("Filter by Tag", ["All"] + list(tag_options.keys()))
if selected_tag == "All":
    df = fetch_df("SELECT * FROM purchases ORDER BY purchase_date DESC;")
else:
    tag_id = tag_options[selected_tag]
    df = fetch_df("""
        SELECT p.*
        FROM purchases p
        JOIN purchase_tags pt ON p.purchase_id = pt.purchase_id
        WHERE pt.tag_id = %s
        ORDER BY p.purchase_date DESC;
    """, (tag_id,))


df = fetch_df("""
    SELECT c.name AS category, SUM(p.amount) AS total
    FROM purchases p
    JOIN categories c ON p.category_id = c.category_id
    GROUP BY c.name
    ORDER BY total DESC;
""")

st.bar_chart(df.set_index("category"))
st.dataframe(df, use_container_width=True)

bills = fetch_df("""
    SELECT name AS category, SUM(amount) AS total
    FROM recurring_bills
    GROUP BY name;
""")

st.subheader("📆 Monthly Bill Obligations")
st.dataframe(bills, use_container_width=True)

st.subheader("All Purchases with Tags")

purchases_with_tags = fetch_df("""
SELECT 
    p.purchase_id,
    p.item,
    p.amount,
    p.purchased_at,
    c.name AS category,
    COALESCE(string_agg(t.tag_name, ', ' ORDER BY t.tag_name), '') AS tags
FROM purchases p
LEFT JOIN categories c ON p.category_id = c.category_id
LEFT JOIN purchase_tags pt ON p.purchase_id = pt.purchase_id
LEFT JOIN tags t ON pt.tag_id = t.tag_id
GROUP BY p.purchase_id, p.item, p.amount, p.purchased_at, c.name
ORDER BY p.purchased_at DESC, p.purchase_id DESC;
""")

st.dataframe(purchases_with_tags)


