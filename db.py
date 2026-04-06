import psycopg2
import pandas as pd
import streamlit as st

def get_connection():
    return psycopg2.connect(st.secrets["DB_URL"])

def fetch_df(query, params=None):
    conn = get_connection()
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

def execute(query, params=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    conn.close()
