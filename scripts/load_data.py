"""
Main data processing script for cleaning and preparing the UCI Online Retail dataset.

Exploratory Data Analysis (EDA) is performed separately in 'scripts/eda.ipynb'.
"""

import os
import pandas as pd

# Define file path relative to this script for portability
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "../Data/global_indicators_raw.xlsx")

# Load raw data
raw_df = pd.read_excel(file_path, sheet_name='Online Retail')

# Create a copy for processing to preserve original data
df = raw_df.copy()

# Remove exact duplicate rows, retaining the first occurrence
df.drop_duplicates(inplace=True)

# Remove rows where Description is missing, UnitPrice is zero, and CustomerID is missing (placeholder transactions)
placeholder_condition = (
    (df["Description"].isnull()) &
    (df["UnitPrice"] == 0.0) &
    (df["CustomerID"].isnull())
)
df.drop(df[placeholder_condition].index, inplace=True)

# Remove problematic invoices identified as extreme negative outliers in UnitPrice
problematic_invoices = ['A563187', 'A563186']
df = df[~df["InvoiceNo"].isin(problematic_invoices)]

# Filter out extreme negative Quantity values, keeping only normal returns (Quantity >= -10)
df = df[df['Quantity'] >= -10]

# Export the cleaned dataset for subsequent loading and analysis
output_csv_path = os.path.join(base_dir, '../Cleaned_data/cleaned_retail_data.csv')
df.to_csv(output_csv_path, index=False)
