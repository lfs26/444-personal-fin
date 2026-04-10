import psycopg2
import psycopg2.extras
import pandas as pd
import streamlit as st


def get_connection():
    return psycopg2.connect(st.secrets["DB_URL"])


def fetch_df(query, params=None):
    """Run a SELECT and return results as a DataFrame."""
    conn = get_connection()
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df


def execute(query, params=None):
    """Run an INSERT/UPDATE/DELETE with no return value."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    cur.close()
    conn.close()


def execute_returning(query, params=None):
    """Run an INSERT ... RETURNING and return the first value of the first row."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    result = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return int(result)  # cast away numpy/psycopg2 type issues
