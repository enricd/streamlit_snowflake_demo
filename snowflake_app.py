import streamlit as st
from datetime import datetime, time
import numpy as np
import pandas as pd

# Snowflake DataBase Bicin Table Schema:

# create or replace ICEBERG TABLE BICING.BICING_SCHEMA.BICING_ICEBERG (
# 	STATION_ID LONG,
# 	NUM_BIKES_AVAILABLE LONG,
# 	MECHANICAL LONG,
# 	EBIKE LONG,
# 	NUM_DOCKS_AVAILABLE LONG,
# 	LAST_REPORTED LONG,
# 	IS_CHARGING_STATION BOOLEAN,
# 	STATUS STRING,
# 	IS_INSTALLED LONG,
# 	IS_RENTING LONG,
# 	IS_RETURNING LONG,
# 	TRAFFIC STRING,
# 	LAST_UPDATED LONG,
# 	TTL LONG,
# 	V1 STRING
# )

st.set_page_config(
    page_title="Bicing Data App",
    page_icon="🚴‍♂️",
    # layout="wide",
)

st.title("🚴‍♂️ Bicing Data App")

conn = st.connection("snowflake")

tabs = st.tabs(["❄️ Database", "📊 Visualizations", "🤖 ML Model"])

# --- Database Tab ---
with tabs[0]:

    # Unique Stations
    unique_stations_query = "SELECT DISTINCT STATION_ID FROM BICING.BICING_SCHEMA.BICING_ICEBERG;"
    unique_stations = conn.query(unique_stations_query, ttl="20m").dropna()["STATION_ID"].map(int).values.tolist()

    # Min and Max Dates
    min_date_query = "SELECT MIN(LAST_UPDATED) FROM BICING.BICING_SCHEMA.BICING_ICEBERG;"
    min_date = conn.query(min_date_query, ttl="20m").dropna()["MIN(LAST_UPDATED)"].values.tolist()[0]
    min_date_dt = datetime.fromtimestamp(min_date)

    max_date_query = "SELECT MAX(LAST_UPDATED) FROM BICING.BICING_SCHEMA.BICING_ICEBERG;"
    max_date = conn.query(max_date_query, ttl="20m").dropna()["MAX(LAST_UPDATED)"].values.tolist()[0]
    max_date_dt = datetime.fromtimestamp(max_date)

    # Select Station and Date Range
    cols_select = st.columns(3)
    with cols_select[0]:
        selected_station = st.selectbox("Select Station", unique_stations, index=0)
    with cols_select[1]:
        start_date = st.date_input("Start Date", min_date_dt, min_value=min_date_dt, max_value=max_date_dt)
        start_date_dt = datetime.combine(start_date, time(0, 0, 0))
    with cols_select[2]:
        end_date = st.date_input("End Date", max_date_dt, min_value=min_date_dt, max_value=max_date_dt)
        end_date_dt = datetime.combine(end_date, time(23, 59, 59))

    # Query the Data
    query = f"""
        SELECT * FROM BICING.BICING_SCHEMA.BICING_ICEBERG
        WHERE STATION_ID = {selected_station}
        AND LAST_UPDATED BETWEEN {int(start_date_dt.timestamp())} AND {int(end_date_dt.timestamp())};
    """

    data_query_df = None
    if st.button("Query Data", type="primary") or True:
        data_query_df = conn.query(query, ttl="20m").dropna()
        data_query_df["LAST_UPDATED"] = pd.to_datetime(data_query_df["LAST_UPDATED"], unit="s")
        st.write(data_query_df)


# --- Visualizations Tab ---
with tabs[1]:
    if data_query_df is None:
        st.warning("Please run a query in the Database tab first.")

    else:
        # Metrics and Line Chart of Mechanical and E-Bike Availability
        st.subheader("📈 Mechanical and E-Bike Availability")

        metrics_cols = st.columns(4)
        metrics_cols[0].metric("Station ID", int(data_query_df["STATION_ID"][0]))
        metrics_cols[1].metric("Avg. Mech. Bikes", int(data_query_df["MECHANICAL"].mean()))
        metrics_cols[2].metric("Avg. E-Bikes", int(data_query_df["EBIKE"].mean()))
        metrics_cols[3].metric("Total Station Docks", int(data_query_df[["NUM_DOCKS_AVAILABLE", "EBIKE", "MECHANICAL"]].iloc[0].sum()))

        st.line_chart(data_query_df[["LAST_UPDATED", "MECHANICAL", "EBIKE"]].set_index("LAST_UPDATED"))

        # Analyze the average availability of e-bikes per hour
        st.subheader("⌚ E-Bike Availability by Hour")

        data_query_df["HOUR"] = data_query_df["LAST_UPDATED"].dt.hour
        hour_analysis_df = data_query_df.groupby("HOUR")["EBIKE"].mean().reset_index().set_index("HOUR")
        st.bar_chart(hour_analysis_df)
        

# --- ML Model Tab ---
with tabs[2]:
    st.subheader("*Mocked Machine Learning Model (fake prediction)*")
    if data_query_df is None:
        st.warning("Please run a query in the Database tab first.")

    else:
        # Loading the model
        from mock_ml_model import MockModel
        model = MockModel()
        st.success("Model Loaded")

        # Data Preprocessing and Prediction
        preds = None
        if st.button("Predict E-Bike Availability", type="primary"):
            with st.spinner("*🧙‍♂️ Inference...*"):
                X = data_query_df[["EBIKE"]].values[-30:]
                preds = model.predict(X)

        if preds is not None:
            # Plot previous e-bike availability and predictions
            st.subheader("🤖 E-Bike Availability Prediction")
            chart_index = np.arange(50)

            # DataFrame with two cols, one for the last 20 values and one for the predictions
            preds = np.array([X.flatten()[-1], *preds])
            chart_data = pd.DataFrame(
                {
                    "Past Data": np.concatenate((X.flatten(), [np.nan] * 20)),
                    "Predictions": np.concatenate(([np.nan] * 29, preds.flatten())),
                    "Index": chart_index,
                }
            ).set_index("Index")
            st.line_chart(chart_data, color=["#0000FF", "#00FF00"])
