import pandas as pd

# Load dataset
file_path = "dataset/superstore_sales.csv"

try:
    df = pd.read_csv(file_path, encoding="latin1")
    print("Dataset loaded successfully!")

except Exception as e:
    print("Error loading dataset:", e)
    exit()

# Display basic information
print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# Convert date columns properly (DD-MM-YYYY)
date_columns = ["Order Date", "Ship Date"]

for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(
            df[col],
            dayfirst=True,
            errors="coerce"
        )

# Fill missing values if any
df.fillna("Unknown", inplace=True)

# Save cleaned dataset
cleaned_file = "dataset/cleaned_superstore_sales.csv"
df.to_csv(cleaned_file, index=False)

print("\nData cleaned successfully!")
print(f"Cleaned file saved as: {cleaned_file}")