import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up page config with custom theme
st.set_page_config(page_title="🚀 Data Sweeper Pro", layout="wide")

# Custom CSS for Glassmorphism & Dark Mode UI
st.markdown("""
    <style>
        body {
            background-color: #0d1117;
            color: white;
            font-family: 'Arial', sans-serif;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        .stButton > button {
            background: linear-gradient(90deg, #ff8a00, #e52e71);
            border-radius: 8px;
            color: white;
            padding: 10px;
            border: none;
            font-size: 16px;
            transition: 0.3s;
        }
        .stButton > button:hover {
            background: linear-gradient(90deg, #e52e71, #ff8a00);
        }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
    <div class='glass-card'>
        <h1 style='text-align:center;'>🚀 Data Sweeper Pro</h1>
        <p style='text-align:center;'>Convert, Clean & Visualize Your Data Seamlessly!</p>
    </div>
""", unsafe_allow_html=True)

# File Upload Section
uploaded_files = st.file_uploader("📂 Upload CSV or Excel Files:", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        # Read File
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        # Display File Info
        st.markdown(f"<div class='glass-card'><h3>📄 {file.name}</h3>", unsafe_allow_html=True)
        st.write(f"**Size:** {file.size / 1024:.2f} KB")
        st.dataframe(df.head())

        # Data Cleaning
        st.subheader("🛠 Data Cleaning Options")
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"🧹 Remove Duplicates ({file.name})"):
                df.drop_duplicates(inplace=True)
                st.success("✅ Duplicates Removed!")
        with col2:
            if st.button(f"🩹 Fill Missing Values ({file.name})"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.success("✅ Missing Values Filled!")

        # Select Specific Columns
        st.subheader("🎯 Select Columns to Keep")
        selected_columns = st.multiselect("Choose Columns", df.columns, default=df.columns)
        df = df[selected_columns]

        # Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"📈 Show Bar Chart ({file.name})"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # File Conversion
        st.subheader("🔄 Convert & Download")
        conversion_type = st.radio("Convert File To:", ["CSV", "Excel"], key=file.name)
        buffer = BytesIO()
        file_name = file.name.replace(file_ext, f".{conversion_type.lower()}")
        mime_type = "text/csv" if conversion_type == "CSV" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        
        if st.button(f"⬇️ Convert & Download {file.name}"):
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
            else:
                df.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)
            st.download_button(
                label=f"📥 Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("🎉 Processing Completed!")