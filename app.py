import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Data-Driven Growth Tool for Small Businesses", layout="wide")

# Title
st.title("📊 Data-Driven Growth Tool for Small Businesses")
st.write("Upload your CSV file to analyze your business performance with filters and insights.")

# Upload CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Show raw data
    st.subheader("📁 Preview of Data")
    st.dataframe(df)

    # Sidebar Filters
    st.sidebar.header("🔍 Filters")

    # Date filter
    date_range = st.sidebar.date_input("Select Date Range", 
        [df['Date'].min(), df['Date'].max()])
    if len(date_range) == 2:
        start_date, end_date = date_range
        df = df[(df['Date'] >= pd.to_datetime(start_date)) & 
                (df['Date'] <= pd.to_datetime(end_date))]

    # Type filter
    type_filter = st.sidebar.multiselect("Select Type", df['Type'].unique(), default=df['Type'].unique())
    df = df[df['Type'].isin(type_filter)]

    # Category filter
    category_filter = st.sidebar.multiselect("Select Category", df['Category'].unique(), default=df['Category'].unique())
    df = df[df['Category'].isin(category_filter)]

    # Summary
    st.subheader("📌 Summary")
    total_revenue = df[df['Type'] == 'Revenue']['Amount'].sum()
    total_expense = df[df['Type'] == 'Expense']['Amount'].sum()
    profit = total_revenue - total_expense

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Revenue", f"₹ {total_revenue:,.0f}")
    col2.metric("💸 Total Expense", f"₹ {total_expense:,.0f}")
    col3.metric("📈 Profit", f"₹ {profit:,.0f}")

    # Pie Chart - Category-wise
    st.subheader("🥧 Category-wise Financial Distribution")
    category_summary = df.groupby(['Category'])['Amount'].sum()
    fig1, ax1 = plt.subplots()
    ax1.pie(category_summary, labels=category_summary.index, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

    # Line Chart - Revenue & Expense Over Time
    st.subheader("📊 Revenue & Expense Over Time")
    line_data = df.groupby(['Date', 'Type'])['Amount'].sum().unstack().fillna(0)
    st.line_chart(line_data)

    # Monthly Profit Bar Chart
    st.subheader("📅 Monthly Profit")
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    monthly_data = df.pivot_table(index='Month', columns='Type', values='Amount', aggfunc='sum').fillna(0)
    monthly_data['Profit'] = monthly_data.get('Revenue', 0) - monthly_data.get('Expense', 0)

    fig2, ax2 = plt.subplots()
    sns.barplot(x=monthly_data.index, y=monthly_data['Profit'], color='skyblue', ax=ax2)
    ax2.set_ylabel("Profit")
    ax2.set_xlabel("Month")
    ax2.set_title("Monthly Profit")
    plt.xticks(rotation=45)
    st.pyplot(fig2)

else:
    st.info("👈 Upload a CSV file to get started.")

