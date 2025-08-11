"""
Main data processing script.

Exploratory Data Analysis (EDA) is done separately in 'scripts/eda.ipynb'.
"""

import os
import pandas as pd

# Build file path relative to this script (portable for Git/GitHub)
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir,"../Data/global_indicators_raw.xlsx")


# Load the data from the xlsx file
raw_df = pd.read_excel(file_path, sheet_name='Online Retail')
df = raw_df.copy()

# Remove exact duplicate rows (keeping the first occurrence)
before_rows = len(df)
df.drop_duplicates(inplace=True)
after_rows = len(df)
print(f"Removed {before_rows - after_rows} duplicate rows.")
