# Financial Data Project

Work in progress — currently building the data cleaning pipeline.  
README will be updated once cleaning and preprocessing steps are complete.


# E-Commerce Sales Data Cleaning & Analysis

Dataset: [UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)  
Transactional data from a UK-based online retailer (1 Dec 2010 – 9 Dec 2011), containing **541,909 rows** and **8 columns** such as InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, and Country.

Goal: Clean, transform, and analyze the dataset using **Python**, **SQL/BigQuery**, **dbt**, and **Looker Studio** to produce business insights and dashboards.

For detailed exploratory data analysis, refer to the [EDA Notebook](scripts/Eda.ipynb).

For safety and reproducibility, I preserve a raw copy of the dataset before performing cleaning steps. This ensures all transformations are traceable and reversible.

## Data Cleaning
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

### Note on Missing CustomerID Values
In this dataset, **133,583 rows** have missing `CustomerID` entries. These were intentionally left as `NaN` rather than replaced with a placeholder like `"Unknown"`.

This decision was made because:

- The number of rows affected is large, and these rows still contain valuable transactional information in other columns. Removing them would result in substantial data loss.
- Keeping them as `NaN` preserves the column’s `float64` data type, avoiding potential compatibility issues during analysis or dashboard creation (e.g., mixing numeric IDs with strings).
- By retaining these rows, we can still leverage them in analyses that don’t require `CustomerID` (e.g., sales trends, product performance) while handling the missing IDs separately if needed.

## Data Type Validation
Verified that all columns have appropriate data types using Python (`df.info()`).  
All numeric, categorical, and datetime columns are correctly typed. No corrections were required.

## Descriptive statistics

### Outlier Detection using IQR (Interquartile Range)

Outliers in numeric data can skew analysis and affect insights. In this project, the IQR method was used to detect outliers in the `UnitPrice` column.  

**Methodology:**
1. Calculate the 25th percentile (Q1) and 75th percentile (Q3) of the column.
2. Compute the Interquartile Range (IQR = Q3 - Q1).
3. Define the lower bound (LB = Q1 - 1.5 * IQR) and upper bound (UB = Q3 + 1.5 * IQR).
4. Any value below LB or above UB is flagged as an outlier.

**Implementation:**
- A reusable function `detect_outliers_iqr()` was created to return the outlier values and bounds.
- For the `UnitPrice` column, the function identified the number of outlier rows.
- Full rows corresponding to these outliers were also extracted for further inspection.

**Example Output for `UnitPrice`:**
Lower Bound: -3.07
Upper Bound: 8.45
Outliers detected: 39450 rows

**Purpose:**
- Detecting outliers ensures the dataset is clean and reliable for analysis and visualization.
- Helps identify unusual transactions or extreme values for further investigation.

### Outlier Detection using Z-score (Revised Function)

Z-score identifies how many standard deviations a value is from the mean. Values with `|z_score| > 3` are considered outliers.

**Methodology:**
1. Calculate the mean and standard deviation of the column (`UnitPrice`).
2. Compute Z-score: `z_score = (value - mean) / std`.
3. Flag rows where `|z_score| > threshold` as outliers.

**Implementation:**
- A reusable function `detect_outliers_z()` was created.
- Returns both the **outlier values** (`Z_Outliers`) and the **full DataFrame rows** (`Z_Outliers_df`), along with mean and std.
**Example Output for `UnitPrice`:**
Mean: 4.645
Standard Deviation: 97.365
Outliers detected: 360 rows


**Purpose:**
- Detects extreme values based on standard deviations.
- Ensures reliable analysis by highlighting unusual transactions.
- Complements IQR-based detection for thorough outlier analysis.

## Graphs

### Histogram: Distribution of Unit Prices

**Key Insights:**
- Most unit prices are clustered at lower values, with a few very high prices.
- Logarithmic y-axis revealed extreme values clearly without distorting the overall distribution.
- Confirms the presence of **outliers**, supporting the IQR and Z-score analysis.
- Ensures the dataset is clean and ready for analysis or dashboards.

### Scatter Plot: Unit Price vs Quantity

**Key Insights:**  
- Most purchases are concentrated at lower quantities and moderate unit prices.  
- A few high-quantity or high-price transactions act as outliers.  
- Color mapping by `CustomerID` highlights patterns of repeat customers.  
- Helps confirm trends and anomalies, ensuring the dataset is clean and ready for analysis or dashboards.

