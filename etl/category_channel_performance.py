import pandas as pd
import json

# Load raw files
sessions = pd.read_csv("C:/Users/kaust/OneDrive/Desktop/Marketing ROI & Budget Reallocation(Project)/data_raw/sessions.csv")
orders = pd.read_csv("C:/Users/kaust/OneDrive/Desktop/Marketing ROI & Budget Reallocation(Project)/data_raw/orders.csv")
order_items = pd.read_csv("C:/Users/kaust/OneDrive/Desktop/Marketing ROI & Budget Reallocation(Project)/data_raw/order_items.csv")

with open("C:/Users/kaust/OneDrive/Desktop/Marketing ROI & Budget Reallocation(Project)/data_raw/products.json", "r", encoding="utf-8") as f:
    products_data = json.load(f)

products = pd.DataFrame(products_data)

# Standardize column names in orders if needed
orders = orders.rename(columns={
    "discount_amount": "discount",
    "shipping_amount": "shipping"
})

# Merge order_items with products to get category
order_product = order_items.merge(products, on="product_id", how="left")

# Merge orders to get session_id
order_product = order_product.merge(
    orders[["order_id", "session_id"]],
    on="order_id",
    how="left"
)

# Merge sessions to get channel
order_product = order_product.merge(
    sessions[["session_id", "channel"]],
    on="session_id",
    how="left"
)

# Create revenue column
# If order_items has line-level amount column, use that.
# Otherwise use quantity * price as a proxy.
if "price" in order_product.columns and "quantity" in order_product.columns:
    order_product["item_revenue"] = order_product["price"] * order_product["quantity"]
else:
    order_product["item_revenue"] = 0

# Aggregate category × channel
category_channel_perf = (
    order_product.groupby(["category", "channel"], dropna=False)
    .agg(
        orders=("order_id", "nunique"),
        revenue=("item_revenue", "sum")
    )
    .reset_index()
)

# Save output
category_channel_perf.to_csv("C:/Users/kaust/OneDrive/Desktop/Marketing ROI & Budget Reallocation(Project)/data/category_channel_performance.csv", index=False)

print("Saved: data/category_channel_performance.csv")
print(category_channel_perf.head())