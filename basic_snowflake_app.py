import streamlit as st

st.title("❄️ Simple Snowflake Query App")

conn = st.connection("snowflake")

# Query the Data
query = """
-- Query for our Bicing Table on Snowflake
SELECT * FROM BICING.BICING_SCHEMA.BICING_ICEBERG
WHERE STATION_ID = 429
LIMIT 50;
"""

st.code(query, language="sql")

data_query_df = conn.query(query, ttl="20m").dropna()
st.write(data_query_df)
