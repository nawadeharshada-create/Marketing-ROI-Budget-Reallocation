import os
import json
import numpy as np
import pandas as pd

# ======================================================
# CONFIG
# ======================================================
RAW_PATH = "C:/Users/kaust/OneDrive/Desktop/Marketing ROI & Budget Reallocation(Project)/data_raw"
OUT_PATH = "C:/Users/kaust/OneDrive/Desktop/Marketing ROI & Budget Reallocation(Project)/data"

os.makedirs(OUT_PATH, exist_ok=True)

# ======================================================
# HELPERS
# ======================================================
def safe_divide(a, b):
    return np.where((pd.isna(b)) | (b == 0), 0, a / b)

def standardize_channel(series):
    return (
        series.astype(str)
        .str.strip()
        .str.lower()
        .replace({
            "paid social": "paid_social",
            "paid-social": "paid_social",
            "e-mail": "email"
        })
    )

# ======================================================
# 1. LOAD RAW FILES
# ======================================================
users = pd.read_csv(f"{RAW_PATH}/users.csv")
campaigns = pd.read_csv(f"{RAW_PATH}/campaigns.csv")
ad_spend_daily = pd.read_csv(f"{RAW_PATH}/ad_spend_daily.csv")
sessions = pd.read_csv(f"{RAW_PATH}/sessions.csv")
orders = pd.read_csv(f"{RAW_PATH}/orders.csv")
order_items = pd.read_csv(f"{RAW_PATH}/order_items.csv")

with open(f"{RAW_PATH}/products.json", "r", encoding="utf-8") as f:
    products_data = json.load(f)
products = pd.DataFrame(products_data)

# ======================================================
# 2. STANDARDIZE COLUMN NAMES
# ======================================================
orders = orders.rename(columns={
    "discount_amount": "discount",
    "shipping_amount": "shipping"
})

# ======================================================
# 3. BASIC CLEANING
# ======================================================
users = users.drop_duplicates()
campaigns = campaigns.drop_duplicates()
ad_spend_daily = ad_spend_daily.drop_duplicates()
sessions = sessions.drop_duplicates()
orders = orders.drop_duplicates()
order_items = order_items.drop_duplicates()
products = products.drop_duplicates()

if "channel" in campaigns.columns:
    campaigns["channel"] = standardize_channel(campaigns["channel"])

if "channel" in ad_spend_daily.columns:
    ad_spend_daily["channel"] = standardize_channel(ad_spend_daily["channel"])

if "channel" in sessions.columns:
    sessions["channel"] = standardize_channel(sessions["channel"])

if "signup_date" in users.columns:
    users["signup_date"] = pd.to_datetime(users["signup_date"], errors="coerce")

if "session_ts" in sessions.columns:
    sessions["session_ts"] = pd.to_datetime(sessions["session_ts"], errors="coerce")

if "order_ts" in orders.columns:
    orders["order_ts"] = pd.to_datetime(orders["order_ts"], errors="coerce")

if "date" in ad_spend_daily.columns:
    ad_spend_daily["date"] = pd.to_datetime(ad_spend_daily["date"], errors="coerce").dt.normalize()

for col in ["spend", "impressions", "clicks"]:
    if col in ad_spend_daily.columns:
        ad_spend_daily[col] = pd.to_numeric(ad_spend_daily[col], errors="coerce").fillna(0)

for col in ["gross_amount", "discount", "shipping", "net_amount"]:
    if col in orders.columns:
        orders[col] = pd.to_numeric(orders[col], errors="coerce").fillna(0)

if "net_amount" in orders.columns:
    q1 = orders["net_amount"].quantile(0.25)
    q3 = orders["net_amount"].quantile(0.75)
    iqr = q3 - q1
    upper_bound = q3 + 1.5 * iqr
    orders["revenue_outlier_flag"] = (orders["net_amount"] > upper_bound).astype(int)
else:
    orders["revenue_outlier_flag"] = 0

# ======================================================
# 4. BUILD fact_sessions.csv
# ======================================================
user_cols = [c for c in ["user_id", "signup_date", "city_tier", "segment", "preferred_device"] if c in users.columns]

fact_sessions = sessions.merge(
    users[user_cols],
    on="user_id",
    how="left"
)

order_join_cols = [c for c in [
    "order_id", "session_id", "order_ts", "gross_amount", "discount", "shipping", "net_amount"
] if c in orders.columns]

fact_sessions = fact_sessions.merge(
    orders[order_join_cols],
    on="session_id",
    how="left"
)

fact_sessions["purchase_flag"] = fact_sessions["order_id"].notna().astype(int)

for col in ["gross_amount", "discount", "shipping", "net_amount"]:
    if col in fact_sessions.columns:
        fact_sessions[col] = fact_sessions[col].fillna(0)

# Derived columns
fact_sessions["session_date"] = pd.to_datetime(fact_sessions["session_ts"], errors="coerce").dt.normalize()

if "signup_date" in fact_sessions.columns:
    fact_sessions["signup_date_only"] = pd.to_datetime(fact_sessions["signup_date"], errors="coerce").dt.normalize()
    fact_sessions["is_new_user"] = (
        fact_sessions["session_date"] == fact_sessions["signup_date_only"]
    ).astype(int)
else:
    fact_sessions["is_new_user"] = 0

if "order_ts" in fact_sessions.columns:
    fact_sessions["session_to_order_hours"] = (
        (fact_sessions["order_ts"] - fact_sessions["session_ts"]).dt.total_seconds() / 3600
    )
else:
    fact_sessions["session_to_order_hours"] = np.nan

# Save a curated output version
fact_sessions_output_cols = [
    "session_id",
    "user_id",
    "session_ts",
    "device",
    "channel",
    "campaign_id",
    "is_new_user",
    "purchase_flag",
    "order_id",
    "gross_amount",
    "discount",
    "net_amount",
    "session_to_order_hours",
    "city_tier",
    "segment",
    "preferred_device"
]
fact_sessions_output_cols = [c for c in fact_sessions_output_cols if c in fact_sessions.columns]
fact_sessions_output = fact_sessions[fact_sessions_output_cols].copy()

# ======================================================
# 5. BUILD ATTRIBUTION LAYER
# ======================================================
campaign_attribution = (
    fact_sessions.groupby(["session_date", "campaign_id", "channel"], dropna=False)
    .agg(
        attributed_sessions=("session_id", "nunique"),
        attributed_orders=("purchase_flag", "sum"),
        attributed_revenue=("net_amount", "sum")
    )
    .reset_index()
    .rename(columns={"session_date": "date"})
)

# ======================================================
# 6. BUILD fact_campaign_daily.csv
# ======================================================
# bring campaign metadata if needed
campaign_meta_cols = [c for c in ["campaign_id", "campaign_name", "objective"] if c in campaigns.columns]
campaigns_meta = campaigns[campaign_meta_cols].drop_duplicates(subset=["campaign_id"])

# If ad_spend_daily doesn't have channel for some reason, fill from campaigns
if "channel" not in ad_spend_daily.columns and "channel" in campaigns.columns:
    ad_spend_daily = ad_spend_daily.merge(
        campaigns[["campaign_id", "channel"]].drop_duplicates(subset=["campaign_id"]),
        on="campaign_id",
        how="left"
    )

fact_campaign_daily = ad_spend_daily.merge(
    campaign_attribution,
    on=["date", "campaign_id", "channel"],
    how="left"
)

for col in ["attributed_sessions", "attributed_orders", "attributed_revenue"]:
    if col in fact_campaign_daily.columns:
        fact_campaign_daily[col] = fact_campaign_daily[col].fillna(0)

fact_campaign_daily = fact_campaign_daily.merge(
    campaigns_meta,
    on="campaign_id",
    how="left"
)

fact_campaign_daily["CPC"] = safe_divide(fact_campaign_daily["spend"], fact_campaign_daily["clicks"])
fact_campaign_daily["CTR"] = safe_divide(fact_campaign_daily["clicks"], fact_campaign_daily["impressions"])
fact_campaign_daily["CVR"] = safe_divide(fact_campaign_daily["attributed_orders"], fact_campaign_daily["attributed_sessions"])
fact_campaign_daily["ROAS"] = safe_divide(fact_campaign_daily["attributed_revenue"], fact_campaign_daily["spend"])
fact_campaign_daily["CAC_proxy"] = safe_divide(fact_campaign_daily["spend"], fact_campaign_daily["attributed_orders"])

fact_campaign_daily_cols = [
    "date",
    "campaign_id",
    "channel",
    "campaign_name",
    "objective",
    "day_idx",
    "promo_flag",
    "spend",
    "impressions",
    "clicks",
    "attributed_sessions",
    "attributed_orders",
    "attributed_revenue",
    "CPC",
    "CTR",
    "CVR",
    "ROAS",
    "CAC_proxy"
]
fact_campaign_daily_cols = [c for c in fact_campaign_daily_cols if c in fact_campaign_daily.columns]
fact_campaign_daily = fact_campaign_daily[fact_campaign_daily_cols].copy()

# ======================================================
# 7. BUILD fact_channel_daily.csv
# ======================================================
group_aggs = {
    "spend": "sum",
    "attributed_orders": "sum",
    "attributed_revenue": "sum"
}
if "promo_flag" in fact_campaign_daily.columns:
    group_aggs["promo_flag"] = "max"

fact_channel_daily = (
    fact_campaign_daily.groupby(["date", "channel"], dropna=False)
    .agg(group_aggs)
    .reset_index()
)

fact_channel_daily = fact_channel_daily.rename(columns={"spend": "total_spend"})

fact_channel_daily["day_of_week"] = pd.to_datetime(fact_channel_daily["date"], errors="coerce").dt.day_name()
fact_channel_daily["week_index"] = (
    (pd.to_datetime(fact_channel_daily["date"], errors="coerce") -
     pd.to_datetime(fact_channel_daily["date"], errors="coerce").min()).dt.days // 7
)

if "promo_flag" not in fact_channel_daily.columns:
    fact_channel_daily["promo_flag"] = 0

fact_channel_daily_cols = [
    "date",
    "channel",
    "total_spend",
    "attributed_orders",
    "attributed_revenue",
    "day_of_week",
    "promo_flag",
    "week_index"
]
fact_channel_daily = fact_channel_daily[fact_channel_daily_cols].copy()

# ======================================================
# 8. EXPORT
# ======================================================
fact_sessions_output.to_csv(f"{OUT_PATH}/fact_sessions.csv", index=False)
fact_campaign_daily.to_csv(f"{OUT_PATH}/fact_campaign_daily.csv", index=False)
fact_channel_daily.to_csv(f"{OUT_PATH}/fact_channel_daily.csv", index=False)

print("ETL completed successfully.")
print("Generated files:")
print(f"- {OUT_PATH}/fact_sessions.csv")
print(f"- {OUT_PATH}/fact_campaign_daily.csv")
print(f"- {OUT_PATH}/fact_channel_daily.csv")