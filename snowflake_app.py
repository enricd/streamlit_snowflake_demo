import streamlit as st

conn = st.connection("snowflake")
df = conn.query("SELECT * FROM BICING.BICING_SCHEMA.BICING_ICEBERG LIMIT 5;", ttl="10m")

st.write(df)

# for row in df.itertuples():
#     st.write(row)