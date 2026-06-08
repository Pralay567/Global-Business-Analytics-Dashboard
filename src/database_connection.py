import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("business_dashboard.db")
cursor = conn.cursor()

# Load cleaned dataset
df = pd.read_csv("dataset/cleaned_superstore_sales.csv")

# Save dataframe to SQL table
df.to_sql("sales_data", conn, if_exists="replace", index=False)

print("Database created successfully!")
print("Data inserted into sales_data table.")

# Close connection
conn.close()