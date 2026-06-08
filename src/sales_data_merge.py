import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dataset_path = os.path.join(BASE_DIR, "dataset")

master_data = []

# -------------------------------
# Global Superstore
# -------------------------------
try:
    df = pd.read_csv(
        os.path.join(dataset_path, "Global Superstore.csv"),
        encoding="latin1",
        low_memory=False
    )

    df = df.rename(columns={
        "Order Date": "Order_Date",
        "Country": "Country",
        "City": "City",
        "Category": "Category",
        "Product Name": "Product_Name",
        "Sales": "Sales",
        "Profit": "Profit",
        "Quantity": "Quantity"
    })

    df = df[[
        "Order_Date",
        "Country",
        "City",
        "Category",
        "Product_Name",
        "Sales",
        "Profit",
        "Quantity"
    ]]

    master_data.append(df)
    print("Global Superstore Loaded")

except Exception as e:
    print("Error:", e)

# -------------------------------
# Amazon Sale Report
# -------------------------------
try:
    df = pd.read_csv(
        os.path.join(dataset_path, "Amazon Sale Report.csv"),
        encoding="latin1",
        low_memory=False
    )

    df = df.rename(columns={
        "Date": "Order_Date",
        "ship-country": "Country",
        "ship-city": "City",
        "Category": "Category",
        "SKU": "Product_Name",
        "Amount": "Sales",
        "Qty": "Quantity"
    })

    df["Profit"] = df["Sales"] * 0.15

    df = df[[
        "Order_Date",
        "Country",
        "City",
        "Category",
        "Product_Name",
        "Sales",
        "Profit",
        "Quantity"
    ]]

    master_data.append(df)
    print("Amazon Report Loaded")

except Exception as e:
    print("Error:", e)

# -------------------------------
# Real World Dataset
# -------------------------------
try:
    df = pd.read_csv(
        os.path.join(
            dataset_path,
            "real_world_sales_dataset_5000.csv"
        ),
        encoding="latin1"
    )

    df = df.rename(columns={
        "Order_Date": "Order_Date",
        "Country": "Country",
        "City": "City",
        "Product_Category": "Category",
        "Product_Name": "Product_Name",
        "Revenue": "Sales",
        "Profit": "Profit",
        "Quantity": "Quantity"
    })

    df = df[[
        "Order_Date",
        "Country",
        "City",
        "Category",
        "Product_Name",
        "Sales",
        "Profit",
        "Quantity"
    ]]

    master_data.append(df)
    print("Real World Dataset Loaded")

except Exception as e:
    print("Error:", e)

# -------------------------------
# Merge Everything
# -------------------------------
merged_df = pd.concat(
    master_data,
    ignore_index=True
)

merged_df.drop_duplicates(inplace=True)

merged_df["Sales"] = pd.to_numeric(
    merged_df["Sales"],
    errors="coerce"
)

merged_df["Profit"] = pd.to_numeric(
    merged_df["Profit"],
    errors="coerce"
)

merged_df.fillna("Unknown", inplace=True)

output_file = os.path.join(
    dataset_path,
    "master_sales_data.csv"
)

merged_df.to_csv(
    output_file,
    index=False
)

print("\nMaster Sales Dataset Created!")
print("Rows:", len(merged_df))
print("Saved:", output_file)