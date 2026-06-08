import pandas as pd
import os

folder = "dataset"

for file in os.listdir(folder):
    if file.endswith(".csv"):

        path = os.path.join(folder, file)

        try:
            df = pd.read_csv(
                path,
                encoding="latin1",
                low_memory=False
            )

            print("\n" + "=" * 60)
            print("FILE:", file)
            print("ROWS:", len(df))
            print("COLUMNS:")

            for col in df.columns:
                print("-", col)

        except Exception as e:
            print(f"Error reading {file}: {e}")