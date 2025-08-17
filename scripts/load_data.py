"""
Main data processing script.

Exploratory Data Analysis (EDA) is done separately in 'scripts/eda.ipynb'.
"""

import os
import pandas as pd

# Build file path relative to this script (portable for Git/GitHub)
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "../Data/global_indicators_raw.xlsx")

# Load the data from the xlsx file
raw_df = pd.read_excel(file_path, sheet_name='Online Retail')
df = raw_df.copy()

# Remove exact duplicate rows (keeping the first occurrence)
df.drop_duplicates(inplace=True)

# Cleaning the 'Description' column
df.drop(
    df[
        (df["Description"].isnull()) &
        (df["UnitPrice"] == 0.0) &
        (df["CustomerID"].isnull())
    ].index,
    inplace=True
)

# Remove problematic invoices identified as extreme negative outliers in UnitPrice
problematic_invoices = ['A563187', 'A563186']
df = df[~df["InvoiceNo"].isin(problematic_invoices)]

# Filter out extreme negative Quantity values (keep only normal returns Quantity >= -10)
df = df[df['Quantity'] >= -10]
