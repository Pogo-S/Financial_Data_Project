import os
import pandas as pd

# Build file path relative to this script (portable for Git/GitHub)
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir,"../data/global_indicators_raw.xlsx")

# exploring file (check sheet names before loading)
xlsx = pd.ExcelFile(file_path)
print(xlsx.sheet_names)