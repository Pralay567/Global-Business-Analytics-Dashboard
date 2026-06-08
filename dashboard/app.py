import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --------------------------------
# Page Config
# --------------------------------
st.set_page_config(
    page_title="Global Business Analytics Dashboard",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Global Business Analytics Dashboard")
st.markdown(
    "Analyze worldwide sales, profit, and product performance"
)

# --------------------------------
# File Path
# --------------------------------
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

file_path = os.path.join(
    BASE_DIR,
    "dataset",
    "master_sales_data.csv"
)

# --------------------------------
# Cached Data Loading
# --------------------------------
@st.cache_data
def load_data(path):

    df = pd.read_csv(
        path,
        low_memory=False
    )

    # Convert numeric columns
    df["Sales"] = pd.to_numeric(
        df["Sales"],
        errors="coerce"
    )

    df["Profit"] = pd.to_numeric(
        df["Profit"],
        errors="coerce"
    )

    df["Quantity"] = pd.to_numeric(
        df["Quantity"],
        errors="coerce"
    )

    # Date conversion
    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"],
        errors="coerce"
    )

    # Remove bad rows
    df.dropna(
        subset=["Sales"],
        inplace=True
    )

    return df


df = load_data(file_path)

# --------------------------------
# Sidebar Filters
# --------------------------------
st.sidebar.header("🌎 Global Filters")

# Country Filter
selected_country = st.sidebar.multiselect(
    "Select Country",
    options=sorted(
        df["Country"]
        .dropna()
        .unique()
    ),
    default=sorted(
        df["Country"]
        .dropna()
        .unique()
    )
)

country_df = df[
    df["Country"]
    .isin(selected_country)
]

# Dynamic City Filter (Faster)
selected_city = st.sidebar.multiselect(
    "Select City",
    options=sorted(
        country_df["City"]
        .dropna()
        .unique()
    ),
    default=[]
)

# Category Filter
selected_category = st.sidebar.multiselect(
    "Select Category",
    options=sorted(
        df["Category"]
        .dropna()
        .unique()
    ),
    default=sorted(
        df["Category"]
        .dropna()
        .unique()
    )
)

# --------------------------------
# Filtering Logic
# --------------------------------
filtered_df = df[
    (df["Country"].isin(selected_country)) &
    (df["Category"].isin(selected_category))
]

# Apply city filter only if selected
if selected_city:
    filtered_df = filtered_df[
        filtered_df["City"]
        .isin(selected_city)
    ]

# --------------------------------
# KPI Metrics
# --------------------------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = len(filtered_df)
avg_sales = filtered_df["Sales"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Sales",
    f"${total_sales:,.0f}"
)

col2.metric(
    "📈 Total Profit",
    f"${total_profit:,.0f}"
)

col3.metric(
    "🛒 Orders",
    f"{total_orders:,}"
)

col4.metric(
    "📦 Avg Sales",
    f"${avg_sales:.2f}"
)

st.divider()

# --------------------------------
# Charts Row
# --------------------------------
col1, col2 = st.columns(2)

# Top Countries Chart
with col1:

    country_sales = (
        filtered_df
        .groupby("Country")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig1 = px.bar(
        country_sales,
        x="Country",
        y="Sales",
        title="🌍 Top Countries by Sales"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

# Category Pie Chart
with col2:

    category_sales = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig2 = px.pie(
        category_sales,
        names="Category",
        values="Sales",
        title="📦 Sales by Category"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# --------------------------------
# Monthly Sales Trend
# --------------------------------
st.subheader("📅 Monthly Sales Trend")

trend_df = filtered_df.copy()

trend_df["Month"] = (
    trend_df["Order_Date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_sales = (
    trend_df
    .groupby("Month")["Sales"]
    .sum()
    .reset_index()
)

fig3 = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="📈 Monthly Global Sales Trend"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# --------------------------------
# Top Products
# --------------------------------
st.subheader("🏆 Top Products")

num_products = st.slider(
    "Select Number of Products",
    min_value=5,
    max_value=50,
    value=10
)

top_products = (
    filtered_df
    .groupby("Product_Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(num_products)
    .reset_index()
)

fig4 = px.bar(
    top_products,
    x="Sales",
    y="Product_Name",
    orientation="h",
    title=f"🏆 Top {num_products} Products"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# --------------------------------
# Footer
# --------------------------------
st.markdown("---")
st.caption(
    "Built using Python, Pandas, Plotly, and Streamlit"
)