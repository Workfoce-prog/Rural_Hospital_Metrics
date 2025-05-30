
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Rural Hospital Dashboard", layout="wide")

st.title("🏥 Rural Hospital Metrics Dashboard")

st.markdown("### 📂 Upload Rural Hospital Data (.xlsx)")
uploaded_file = st.file_uploader("Choose a file", type="xlsx")

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

    st.subheader("📊 Visualization: Top 5 by Patient Satisfaction")
    top5_satisfaction = df.sort_values("Patient Satisfaction (1-5)", ascending=False).head(5)
    st.bar_chart(top5_satisfaction.set_index("Hospital Name")["Patient Satisfaction (1-5)"])

    st.subheader("📉 Visualization: ER Wait Time by Hospital")
    st.line_chart(df.set_index("Hospital Name")["ER Wait Time (mins)"])

    st.subheader("🟠 Pie Chart: Readmission Rate Categories")
    def label_rag(rate):
        if rate < 10:
            return "Green"
        elif rate < 15:
            return "Amber"
        else:
            return "Red"
    df["Readmission RAG"] = df["30-Day Readmission Rate (%)"].apply(label_rag)
    st.pyplot(df["Readmission RAG"].value_counts().plot.pie(autopct='%1.1f%%', title="RAG Categories").figure)
else:
    st.info("📁 Please upload a rural hospital data file to begin.")
