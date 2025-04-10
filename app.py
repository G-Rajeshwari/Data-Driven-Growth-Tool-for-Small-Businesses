import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(
    page_title="Data-Driven Growth Tool for Small Businesses",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom header with centered text and emoji
st.markdown("<h1 style='text-align: center;'>📊 Data-Driven Growth Tool</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Upload your business data to gain visual insights on revenue, expenses, and profits.</p>", unsafe_allow_html=True)
st.markdown("---")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📁 Preview of Uploaded Data")
    st.dataframe(df.head())

    # Sidebar filters (optional enhancement)
    st.sidebar.header("Filters")
    numeric_columns = df.select_dtypes(include='number').columns.tolist()

    if numeric_columns:
        selected_column = st.sidebar.selectbox("Choose a numeric column to plot", numeric_columns)

        st.markdown(f"### 📉 Bar Plot for `{selected_column}`")

        fig, ax = plt.subplots()
        sns.barplot(x=df.index, y=df[selected_column], color='skyblue', ax=ax)
        ax.set_ylabel(selected_column)
        ax.set_xlabel("Index")
        st.pyplot(fig)
    else:
        st.warning("No numeric columns found in the uploaded file.")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: 0.85em;'>Created by G-Rajeshwari | Expo 2025</p>",
    unsafe_allow_html=True
)
