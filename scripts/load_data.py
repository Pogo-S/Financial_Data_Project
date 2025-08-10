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
df = pd.read_excel(file_path, sheet_name='Online Retail')

