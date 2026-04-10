import streamlit as st
from db import fetch_df

st.title("📈 Spending Summary")

# -------------------------
# TAG FILTER
# -------------------------
tag_df = fetch_df("SELECT tag_id, tag_name FROM tags ORDER BY tag_name;")
tag_options = {row["tag_name"]: row["tag_id"] for _, row in tag_df.iterrows()}

selected_tag = st.selectbox("Filter by Tag", ["All"] + list(tag_options.keys()))

# -------------------------
# CATEGORY SUMMARY
# -------------------------
st.subheader("📊 Spending by Category")

category_summary = fetch_df("""
    SELECT c.name AS category, SUM(p.amount) AS total
    FROM purchases p
    JOIN categories c ON p.category_id = c.category_id
    GROUP BY c.name
    ORDER BY total DESC;
""")

st.bar_chart(category_summary.set_index("category"))
st.dataframe(category_summary, use_container_width=True)

# -------------------------
# MONTHLY BILLS
# -------------------------
st.subheader("📆 Monthly Bill Obligations")

bills = fetch_df("""
    SELECT name AS category, SUM(amount) AS total
    FROM recurring_bills
    GROUP BY name;
""")

st.dataframe(bills, use_container_width=True)

# -------------------------
# PURCHASES WITH TAGS (FILTERABLE)
# -------------------------
st.subheader("🧾 All Purchases with Tags")

if selected_tag == "All":
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
else:
    tag_id = tag_options[selected_tag]
    purchases_with_tags = fetch_df("""
        SELECT 
            p.purchase_id,
            p.item,
            p.amount,
            p.purchased_at,
            c.name AS category,
            COALESCE(string_agg(t.tag_name, ', ' ORDER BY t.tag_name), '') AS tags
        FROM purchases p
        JOIN purchase_tags pt ON p.purchase_id = pt.purchase_id
        JOIN tags t ON pt.tag_id = t.tag_id
        LEFT JOIN categories c ON p.category_id = c.category_id
        WHERE pt.tag_id = %s
        GROUP BY p.purchase_id, p.item, p.amount, p.purchased_at, c.name
        ORDER BY p.purchased_at DESC, p.purchase_id DESC;
    """, (tag_id,))

st.dataframe(purchases_with_tags, use_container_width=True)
