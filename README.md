# 📊 Marketing ROI & Budget Reallocation

> **An end-to-end marketing analytics solution** combining ETL pipelines, attribution modeling, and regression analysis to optimize channel performance and budget allocation — with insights visualized in an interactive Power BI dashboard.

---

## 📌 Table of Contents

- [Project Overview](#project-overview)
- [North Star Metric](#north-star-metric)
- [Supporting KPIs](#supporting-kpis)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Attribution Model](#attribution-model)
- [How to Run](#how-to-run)
- [Curated Outputs](#curated-outputs)
- [Dashboard](#dashboard)
- [Key Findings](#key-findings)
- [Future Improvements](#future-improvements)

---

## 🔍 Project Overview

This project analyzes marketing spend and revenue performance across multiple channels (Search, Email, Paid Social, etc.) to answer one core business question:

> **"Where should we put our marketing budget to get the most revenue?"**

The analysis pipeline includes:

- **ETL** — Raw data extraction, transformation, and loading into clean datasets
- **Attribution Modeling** — Crediting revenue to the right marketing channel
- **Regression Analysis** — Estimating the incremental revenue impact of each channel
- **Budget Reallocation** — Data-driven recommendations for optimal spend distribution
- **Power BI Dashboard** — Interactive visualization of all insights

---

## 🎯 North Star Metric

### `Incremental Revenue per ₹ Spent`

This metric was chosen because it:

1. Directly measures the **efficiency** of marketing spend
2. Allows **fair comparison** across channels with different budget sizes
3. Drives better **budget reallocation** decisions

---

## 📈 Supporting KPIs

| KPI | Formula | Purpose |
|---|---|---|
| Total Revenue | Sum of all revenue | Measure overall growth |
| Total Spend | Sum of all channel spend | Track budget usage |
| ROAS | Revenue / Spend | Return on ad spend |
| CAC | Spend / Orders | Cost to acquire a customer |
| Conversion Rate | Orders / Sessions | Channel efficiency |
| Revenue per Session | Revenue / Sessions | Session quality |
| AOV | Revenue / Orders | Average order size |
| Discount Rate | Discounts / Revenue | Pricing health |
| Channel Mix Share | Channel Spend / Total Spend | Budget distribution |
| New vs Returning | Segment-wise performance | Audience quality |

---

## 📁 Project Structure

```
Marketing-ROI-Budget-Reallocation/
│
├── data_raw/                        # Raw input data (source files)
│
├── etl/                             # ETL scripts
│   ├── category_channel_performance.py
│   └── part_e_regression.ipynb
│
├── data/                            # Cleaned & curated datasets (ETL outputs)
│   ├── fact_sessions.csv
│   ├── fact_orders.csv
│   ├── fact_campaign_daily.csv
│   ├── fact_channel_daily.csv
│   └── category_channel_performance.csv
│
├── analysis/                        # Analysis notebooks
│
├── dashboard/                       # Power BI dashboard (.pbix file)
│
├── final_story/                     # Final business insights & storytelling
│
├── requirements.txt                 # Python dependencies
└── README.md
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.x | ETL scripts & regression analysis |
| Pandas | Data transformation & aggregation |
| Scikit-learn | Regression modeling |
| Matplotlib / Seaborn | Exploratory visualizations |
| Jupyter Notebook | Interactive analysis |
| Power BI | Final dashboard |

---

## 🔗 Attribution Model

**Method Used: Last-Touch Attribution**

The final marketing channel a customer interacts with before converting receives **100% credit** for that revenue.

**Why Last-Touch?**
- Simple and interpretable for stakeholders
- Directly identifies channels that **close conversions**
- Works well when the goal is optimizing bottom-of-funnel performance

**Limitation:** Does not account for channels that influence the customer earlier in the journey (awareness, consideration stages).

> ⚠️ Future scope: Multi-touch attribution (Linear, Time-Decay, Shapley Values) for a more complete picture.

---

## ▶️ How to Run

### Prerequisites

Install required Python packages:

```bash
pip install -r requirements.txt
```

### Step 1 — Clone the Repository

```bash
git clone https://github.com/nawadeharshada-create/Marketing-ROI-Budget-Reallocation.git
cd Marketing-ROI-Budget-Reallocation
```

### Step 2 — Run ETL Scripts

```bash
# Run channel performance ETL
python etl/category_channel_performance.py

# Run regression analysis notebook
jupyter execute etl/part_e_regression.ipynb
```

### Step 3 — Check Outputs

Cleaned datasets will be generated inside `/data/`:

```
data/
├── fact_sessions.csv
├── fact_orders.csv
├── fact_campaign_daily.csv
├── fact_channel_daily.csv
└── category_channel_performance.csv
```

### Step 4 — Open Dashboard

Open `dashboard/Marketing_ROI_Dashboard.pbix` in **Power BI Desktop**.

---

## 📦 Curated Outputs

| File | Description |
|---|---|
| `fact_sessions.csv` | Session-level data per channel and date |
| `fact_orders.csv` | Order-level data with revenue and discounts |
| `fact_campaign_daily.csv` | Daily campaign performance metrics |
| `fact_channel_daily.csv` | Daily aggregated channel performance |
| `category_channel_performance.csv` | Category-wise channel breakdown |

These files power both the analysis notebooks and the Power BI dashboard.

---

## 📊 Dashboard

Built in **Power BI**, the dashboard contains 4 report pages:

| Page | What It Shows |
|---|---|
| Executive Summary | High-level KPIs — Revenue, ROAS, CAC, Conversion Rate |
| Channel & Campaign Performance | Channel-wise spend vs revenue comparison |
| Attribution vs Regression Analysis | Last-touch vs regression-estimated revenue contribution |
| Segments & Opportunities | New vs returning users, underperforming channels |


---

## 💡 Key Findings

- ✅ **Search & Email** are the highest-performing channels with strong ROAS and low CAC
- ⚠️ **Paid Social** shows inefficiencies — high CAC with relatively low conversion rates
- 📉 Budget was over-allocated to underperforming channels relative to revenue contribution
- 💰 Proposed budget reallocation is estimated to generate a **~X% revenue uplift over 30 days**

> *(Replace X% with your actual estimated figure from the regression model)*

---

## 🚀 Future Improvements

- [ ] Implement **multi-touch attribution** (Linear, Time-Decay, Shapley Values)
- [ ] Build a **Marketing Mix Model (MMM)** using regression to isolate channel effects
- [ ] Automate the ETL pipeline with **Airflow or Prefect**
- [ ] Deploy an **interactive web dashboard** using Streamlit or Plotly Dash
- [ ] Add **statistical significance testing** for budget reallocation recommendations

---

## 👤 Author

**Harshada Nawade**
📧 nawadeharshada@gmail.com
🔗 www.linkedin.com/in/harshada-nawade-6b7617256

---

## 📄 License

This project is for educational and portfolio purposes.
