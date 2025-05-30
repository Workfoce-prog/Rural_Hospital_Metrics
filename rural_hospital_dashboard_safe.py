
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Rural Hospital Dashboard", layout="wide")

st.title("🏥 Rural Hospital Metrics Dashboard")

st.markdown("### 📂 Upload Rural Hospital Data (.xlsx)")
uploaded_file = st.file_uploader("Choose a file", type="xlsx")

# Define required columns
required_columns = [
    "Hospital Name",
    "30-Day Readmission Rate (%)",
    "Patient Satisfaction (1-5)",
    "ER Wait Time (mins)",
    "Operating Margin (%)"
]

# Load default data for fallback
def load_mock_data():
    return pd.DataFrame({
        "Hospital Name": ["Alpha Clinic", "Beta Center", "Gamma Medical"],
        "30-Day Readmission Rate (%)": [12, 18, 9],
        "Patient Satisfaction (1-5)": [4.1, 3.6, 4.5],
        "ER Wait Time (mins)": [30, 70, 40],
        "Operating Margin (%)": [2.5, -4.0, 1.2]
    })

# Load data
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    if all(col in df.columns for col in required_columns):
        st.success("✅ File uploaded and validated!")
    else:
        st.warning("⚠️ Uploaded file is missing required columns. Using mock data.")
        df = load_mock_data()
else:
    st.info("📁 Please upload a rural hospital data file to begin. Using mock data as preview.")
    df = load_mock_data()

st.subheader("📊 Data Table")
st.dataframe(df)

st.subheader("📈 KPI Highlights")
st.metric("Avg. Readmission Rate (%)", round(df["30-Day Readmission Rate (%)"].mean(), 2))
st.metric("Avg. Operating Margin (%)", round(df["Operating Margin (%)"].mean(), 2))
st.metric("Avg. ER Wait Time (mins)", round(df["ER Wait Time (mins)"].mean(), 2))
st.metric("Avg. Patient Satisfaction", round(df["Patient Satisfaction (1-5)"].mean(), 2))

st.subheader("📊 Top 5 by Patient Satisfaction")
top5 = df.sort_values("Patient Satisfaction (1-5)", ascending=False).head(5)
st.bar_chart(top5.set_index("Hospital Name")["Patient Satisfaction (1-5)"])

st.subheader("📉 ER Wait Time by Hospital")
st.line_chart(df.set_index("Hospital Name")["ER Wait Time (mins)"])

st.subheader("🟠 Readmission Rate Category (Pie)")
def rag_category(rate):
    if rate < 10:
        return "Green"
    elif rate < 15:
        return "Amber"
    else:
        return "Red"
df["Readmission Category"] = df["30-Day Readmission Rate (%)"].apply(rag_category)
st.pyplot(df["Readmission Category"].value_counts().plot.pie(autopct='%1.1f%%', title="RAG Categories").figure)
