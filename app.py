import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="📊 Data-Driven Growth Tool for Small Businesses",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to hide Streamlit footer and fine-tune layout
st.markdown("""
    <style>
        footer {visibility: hidden;}
        .block-container {padding-top: 1rem;}
        h1 {color: #2E86C1;}
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📊 Data-Driven Growth Tool for Small Businesses")
st.write("Upload your CSV file to analyze your business performance with filters and insights.")

# Upload CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df.dropna(subset=['Date'], inplace=True)

    # Sidebar Filters
    st.sidebar.header("🔍 Filters")

    # Date Filter
    date_range = st.sidebar.date_input("Select Date Range", [df['Date'].min(), df['Date'].max()])
    if len(date_range) == 2:
        start_date, end_date = date_range
        df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

    # Type Filter
    type_filter = st.sidebar.multiselect("Select Type", df['Type'].unique(), default=df['Type'].unique())
    df = df[df['Type'].isin(type_filter)]

    # Category Filter
    category_filter = st.sidebar.multiselect("Select Category", df['Category'].unique(), default=df['Category'].unique())
    df = df[df['Category'].isin(category_filter)]

    # Preview Data
    st.subheader("📁 Preview of Filtered Data")
    st.dataframe(df, use_container_width=True)

    # Summary
    st.subheader("📌 Summary")
    total_revenue = df[df['Type'] == 'Revenue']['Amount'].sum()
    total_expense = df[df['Type'] == 'Expense']['Amount'].sum()
    profit = total_revenue - total_expense

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Revenue", f"₹ {total_revenue:,.0f}")
    col2.metric("💸 Total Expense", f"₹ {total_expense:,.0f}")
    col3.metric("📈 Profit", f"₹ {profit:,.0f}")

    # Category-wise Pie Chart
    st.subheader("🥧 Category-wise Financial Distribution")
    if not df.empty:
        category_summary = df.groupby('Category')['Amount'].sum()
        fig1, ax1 = plt.subplots()
        ax1.pie(category_summary, labels=category_summary.index, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)
    else:
        st.warning("No data available for pie chart.")

    # Revenue & Expense Over Time Line Chart
    st.subheader("📊 Revenue & Expense Over Time")
    if not df.empty:
        time_series = df.groupby(['Date', 'Type'])['Amount'].sum().unstack().fillna(0)
        st.line_chart(time_series)
    else:
        st.warning("No data available for line chart.")

    # Monthly Profit Bar Chart
    st.subheader("📅 Monthly Profit")
    if not df.empty:
        df['Month'] = df['Date'].dt.to_period('M').astype(str)
        monthly = df.pivot_table(index='Month', columns='Type', values='Amount', aggfunc='sum').fillna(0)
        monthly['Profit'] = monthly.get('Revenue', 0) - monthly.get('Expense', 0)

        fig2, ax2 = plt.subplots(figsize=(10, 4))
        sns.barplot(x=monthly.index, y=monthly['Profit'], color='skyblue', ax=ax2)
        ax2.set_ylabel("Profit (₹)")
        ax2.set_xlabel("Month")
        ax2.set_title("Monthly Profit")
        plt.xticks(rotation=45)
        st.pyplot(fig2)
    else:
        st.warning("No data available for bar chart.")
else:
    st.info("👈 Please upload a CSV file to get started.")
