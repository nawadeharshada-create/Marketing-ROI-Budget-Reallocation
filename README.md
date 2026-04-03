# Marketing ROI & Budget Reallocation Project #

## Project Overview

This project focuses on analyzing marketing performance and optimizing budget allocation across different channels to maximize revenue and improve efficiency.

The analysis combines:

Attribution modeling
Regression-based impact estimation
Dashboard visualization

## North Star Metric

Incremental Revenue per ₹ Spent

This metric is chosen because:

1. It directly measures efficiency of marketing spend
2. Helps compare channels fairly
3. Supports better budget reallocation decisions


## Supporting KPIs

1. Total Revenue
2. Total Spend
3. ROAS (Revenue / Spend)
4. CAC (Spend / Orders)
5. Conversion Rate (Orders / Sessions)
6. Revenue per Session
7. AOV (Average Order Value)
8. Discount Rate
9. Channel Mix Share (Spend & Revenue)
10. New vs Returning User Performance


## Attribution Method Used

Last-Touch Attribution Model

The final channel before conversion gets full credit for revenue
Helps identify which channels directly drive conversions

## How to Run ETL End-to-End

Step 1 — Navigate to project folder
cd Marketing ROI & Budget Reallocation(Project)

Step 2 — Run ETL scripts
python category_channel_performance.py
python part_e_regression.ipynb

Step 3 — Generated outputs
ETL will create cleaned datasets inside:
/data

# Curated Outputs Generated
fact_sessions.csv
fact_orders.csv
fact_campaign_daily.csv
fact_channel_daily.csv
category_channel_performance.csv

# These are used for:
Analysis
Dashboard creation
 
# Dashboard Tool Used
Power BI

# Dashboard Includes
Executive Summary
Channel & Campaign Performance
Attribution vs Regression Analysis
Segments & Opportunities

# Key Outcomes
Identified high-performing channels (Search, Email)
Detected inefficiencies in Paid Social (high CAC)
Proposed optimized budget allocation
Estimated 30-day revenue uplift

# Key Outcomes
Identified high-performing channels (Search, Email)
Detected inefficiencies in Paid Social (high CAC)
Proposed optimized budget allocation
Estimated 30-day revenue uplift

