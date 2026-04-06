import streamlit as st
from db import fetch_df

st.title("📈 Spending Summary")

df = fetch_df("""
    SELECT c.name AS category, SUM(p.amount) AS total
    FROM purchases p
    JOIN categories c ON p.category_id = c.category_id
    GROUP BY c.name
    ORDER BY total DESC;
""")

st.bar_chart(df.set_index("category"))
st.dataframe(df, use_container_width=True)
