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
- Most unit prices are clustered at very low values, with a few transactions at extremely high prices.  
- Applied a **logarithmic y-axis** to reveal rare but extreme values without losing visibility of the dense lower range.  
- Confirms the presence of **outliers**, supporting both IQR- and Z-score-based detection methods.  
- Helps in understanding the spread of pricing data before cleaning and analysis.  

---

### Violin Plot: Distribution of Z-Scores

**Key Insights:**
- Z-score shows how many standard deviations a value is away from the mean.  
- Horizontal dashed lines at `+3` and `-3` mark the **outlier thresholds**.  
- Most data points lie close to the center (within -3 to +3), while extreme tails clearly highlight outliers.  
- The plot provides an intuitive view of the **concentration of normal values vs. extreme anomalies**.  
- Complements the histogram by focusing on statistical deviation rather than raw values.  

## Handling Extreme Outliers

### Extreme Positive Outliers in `UnitPrice`

Using **Z-score analysis**, we identified several rows with extremely high `UnitPrice` values.  
The top 20 entries (highest Z-scores) include prices ranging from **$6,497** up to **$38,970**, corresponding to Z-scores as high as **400**.

**Examples of detected outliers:**
| InvoiceNo | StockCode | Description  | Quantity | UnitPrice | CustomerID | Country         | Z-Score |
|-----------|-----------|--------------|----------|-----------|------------|----------------|---------|
| 222681    | C556445   | Manual       | -1       | $38,970.00 | 15098.0    | United States  | 400.20  |
| 524602    | C580605   | AMAZONFEE    | -1       | $17,836.46 | NaN        | United States  | 183.14  |
| 43702     | C540117   | AMAZONFEE    | -1       | $16,888.02 | NaN        | United States  | 173.40  |
| 173382    | 551697    | POSTAGE      | 1        | $8,142.75  | 16029.0    | United States  | 83.58   |
| 262414    | C559917   | AMAZONFEE    | -1       | $6,497.47  | NaN        | United States  | 66.69   |

**Observations:**
- Many of these transactions are linked to **service-related items** such as:
  - `AMAZONFEE` (Amazon marketplace fees)  
  - `POSTAGE` (shipping/handling charges)  
  - `Manual` adjustments  
  - `Adjust bad debt`  
- Since this dataset is about an **online retailer**, these unusually high `UnitPrice` values reflect **valid operational costs** (e.g., large postage charges, external marketplace fees).  
- These values are therefore **not data errors**.

**Conclusion:**  
Although statistically extreme, these entries are valid and provide important context for financial and operational analysis.  
Hence, **extreme positive values are retained** in the dataset for accuracy.

### Extreme Negative Outliers in `UnitPrice` and Extreme Negative `Quantity`

#### Problematic Invoice Rows (Extreme Negative `UnitPrice`)

During my initial analysis, I identified two specific invoices as **problematic outliers** based on Z-score analysis of `UnitPrice`:

- **InvoiceNo:** `A563187`  
- **InvoiceNo:** `A563186`  

These rows had extreme negative `UnitPrice` values and were inconsistent with normal online retail activity. To maintain data quality, I decided to remove them from the dataset.

#### Handling Negative and Extreme Quantity Values

During my initial exploration, I noticed that the dataset contains **negative values in the `Quantity` column**. At first, I understood these as **normal returns or cancellations**, which are expected in retail data.  

However, during further analysis, I observed that some negative quantities were **extremely large**, going as low as `-80,995`. These extreme negative values are not realistic for typical sales and are likely **bulk adjustments, stock corrections, or data entry errors**.
**Note:**
Initially, there were 9,725 rows with negative quantities, ranging from `-1` to `-80,995`. After filtering to retain only normal returns (quantities ≥ -10), the number of negative rows reduced to 7,642, with quantities now ranging from `-10` to `-1`. This step helped preserve meaningful sales and return data while removing extreme negative transactions that could distort analysis.







> ⚠️ **Reminder:** Before finalizing the README, make sure to change all instances of "we" to "I" to reflect that this project is done individually.
