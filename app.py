import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Small Business Data Viewer")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV
    df = pd.read_csv(uploaded_file)
    
    st.subheader("Preview of Data")
    st.write(df.head())

    # Plot
    st.subheader("📈 Sample Bar Plot")
    col_options = df.select_dtypes(include='number').columns.tolist()

    if col_options:
        col = st.selectbox("Choose a numeric column to plot", col_options)
        st.bar_chart(df[col])
    else:
        st.warning("No numeric columns to plot.")
else:
    st.info("Please upload a CSV file to get started.")
