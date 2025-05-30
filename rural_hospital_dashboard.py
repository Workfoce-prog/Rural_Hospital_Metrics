
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Rural Hospital Dashboard", layout="wide")

st.title("🏥 Rural Hospital Metrics Dashboard")

uploaded_file = st.file_uploader("Upload Rural Hospital Data (.xlsx)", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📊 Uploaded Data")
    st.dataframe(df)

    st.subheader("🟢 High-Performing Hospitals (Based on Readmission and Satisfaction)")
    good_perf = df[(df["30-Day Readmission Rate (%)"] < 15) & (df["Patient Satisfaction (1-5)"] >= 4.0)]
    st.dataframe(good_perf)

    st.subheader("🔴 Hospitals Needing Attention (Low Operating Margin or Long ER Wait)")
    risk = df[(df["Operating Margin (%)"] < 0) | (df["ER Wait Time (mins)"] > 60)]
    st.dataframe(risk)

    st.subheader("📈 KPI Highlights")
    st.metric("Avg. Readmission Rate (%)", round(df["30-Day Readmission Rate (%)"].mean(), 2))
    st.metric("Avg. Operating Margin (%)", round(df["Operating Margin (%)"].mean(), 2))
    st.metric("Avg. ER Wait Time (mins)", round(df["ER Wait Time (mins)"].mean(), 2))
    st.metric("Avg. Patient Satisfaction", round(df["Patient Satisfaction (1-5)"].mean(), 2))
else:
    st.info("Please upload a rural hospital data file to begin.")
