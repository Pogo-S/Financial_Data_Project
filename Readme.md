# Financial Data Project

Work in progress — currently building the data cleaning pipeline.  
README will be updated once cleaning and preprocessing steps are complete.


# E-Commerce Sales Data Cleaning & Analysis

Dataset: [UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)  
Transactional data from a UK-based online retailer (1 Dec 2010 – 9 Dec 2011), containing **541,909 rows** and **8 columns** such as InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, and Country.

Goal: Clean, transform, and analyze the dataset using **Python**, **SQL/BigQuery**, **dbt**, and **Looker Studio** to produce business insights and dashboards.

For detailed exploratory data analysis, refer to the [EDA Notebook](scripts/Eda.ipynb).

For safety and reproducibility, I preserve a raw copy of the dataset before performing cleaning steps. This ensures all transformations are traceable and reversible.

### Data Cleaning
- Added duplicate detection and removal in both the **EDA notebook** (`scripts/eda.ipynb`) and **main processing script** (`scripts/your_script.py`).
- Duplicates are removed across all columns, keeping the first occurrence of each row.
- The number of rows removed is displayed when running the main script.


### Cleaning Missing `Description` Values

Identified and removed 1,454 rows where:
- `Description` was missing (`NaN`)
- `UnitPrice` was `0.0`
- `CustomerID` was missing (`NaN`)

These records appeared to be non-usable placeholder transactions with no meaningful product or customer information.

**Impact:**  
- **Total rows before removal:** 536,641  
- **Total rows after removal:** 535,187  
- **Rows removed:** 1,454  

**Note:**  
An alternative approach considered was filling missing `Description` values using their `StockCode`. However, a single `StockCode` can correspond to multiple product descriptions, making automatic filling unreliable.  

### Next Steps
- Handle missing values in`CustomerID`.
- Standardize data types (e.g., convert `CustomerID` to integer/string where possible).
- Further exploration for potential outliers.