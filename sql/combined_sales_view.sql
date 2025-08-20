CREATE OR REPLACE VIEW `retail-data-pipeline-469519.retail_data.combined_sales` AS

SELECT
  Country,
  EXTRACT(YEAR FROM InvoiceDate) AS Year,
  EXTRACT(MONTH FROM InvoiceDate) AS Month,
  StockCode,
  Description,
  SUM(Quantity * UnitPrice) AS Revenue
FROM
  `retail-data-pipeline-469519.retail_data.cleaned_retail`
GROUP BY
  Country,
  Year,
  Month,
  StockCode,
  Description;
