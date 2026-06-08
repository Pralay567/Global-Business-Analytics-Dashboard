import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("business_dashboard.db")

# Load data
query = "SELECT * FROM sales_data"
df = pd.read_sql(query, conn)

# Convert columns to numeric
df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")

# KPIs
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order ID"].nunique()
avg_sales = df["Sales"].mean()

# Top category
top_category = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
)

print("\n===== BUSINESS KPI REPORT =====")
print(f"Total Sales: ${total_sales:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Total Orders: {total_orders}")
print(f"Average Sales: ${avg_sales:,.2f}")
print(f"Top Category: {top_category}")

# Region-wise sales
print("\n===== REGION SALES =====")
region_sales = (
    df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(region_sales)

conn.close()