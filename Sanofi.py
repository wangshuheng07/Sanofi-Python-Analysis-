import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Read Excel files
file_path = "/Users/shuheng/Downloads/Product_Usage_Analysis.xlsx"
file_path2 = "/Users/shuheng/Downloads/Segmentation_Data_Export.xlsx"
product_usage = pd.read_excel(file_path)
segmentation = pd.read_excel(file_path2)

# Data cleaning
product_usage = product_usage.dropna(subset=['Count of events', 'Amount (In Cents)'])
product_usage['Date'] = pd.to_datetime(product_usage['Date'], errors='coerce')

# Data merging
merged_data = product_usage.merge(segmentation, on="Merchant", how="left")

# Group by product summary
product_summary = merged_data.groupby('Product').agg(
    Total_Events=('Count of events', 'sum'),
    Total_Revenue=('Amount (In Cents)', 'sum'),
    Average_Revenue=('Amount (In Cents)', 'mean')
).reset_index()

# Group by segment summary
segment_summary = merged_data.groupby('Segment').agg(
    Total_Events=('Count of events', 'sum'),
    Total_Revenue=('Amount (In Cents)', 'sum')
).reset_index()

# Group by overall time series
time_series_data = product_usage.groupby('Date').agg(
    Total_Revenue=('Amount (In Cents)', 'sum'),
    Total_Events=('Count of events', 'sum')
).reset_index()

# Define a function to format numbers as billions
def billions(x, pos):
    return f'{x * 1e-9:.1f}B'

# Set Y-axis formatter
formatter = FuncFormatter(billions)

# Visualization: Total Revenue by Product
colors = ['red', 'green', 'blue', 'orange']
fig, ax = plt.subplots()
ax.bar(product_summary['Product'], product_summary['Total_Revenue'], color=colors)
ax.set_title('Total Revenue by Product')
ax.set_xlabel('Product')
ax.set_ylabel('Total Revenue')
ax.yaxis.set_major_formatter(formatter)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Visualization: Line charts for overall trends
for metric, title, ylabel in zip(
    ['Total_Revenue', 'Total_Events'],
    ['Total Revenue Over Time (Overall)', 'Total Events Over Time (Overall)'],
    ['Total Revenue', 'Total Events']
):
    plt.figure(figsize=(10, 6))
    plt.plot(time_series_data['Date'], time_series_data[metric], marker='o', label=title)
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Visualization for each product dynamically
products = product_usage['Product'].unique()
colors = ['green', 'purple', 'orange', 'cyan', 'red', 'blue', 'brown', 'pink']  # Assign colors dynamically

for idx, product in enumerate(products):
    filtered_data = product_usage[product_usage['Product'] == product]
    product_time_series = filtered_data.groupby('Date').agg(
        Total_Revenue=('Amount (In Cents)', 'sum'),
        Total_Events=('Count of events', 'sum')
    ).reset_index()

    # Line charts for revenue and events
    for metric, color, title in zip(
        ['Total_Revenue', 'Total_Events'],
        [colors[idx % len(colors)], colors[(idx + 1) % len(colors)]],
        [f'Total Revenue Over Time ({product})', f'Total Events Over Time ({product})']
    ):
        plt.figure(figsize=(10, 6))
        plt.plot(product_time_series['Date'], product_time_series[metric], marker='o', color=color, label=title)
        plt.title(title)
        plt.xlabel('Date')
        plt.ylabel('Revenue' if metric == 'Total_Revenue' else 'Events')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

# Scatter plot for each product
for product in products:
    filtered_data = product_usage[product_usage['Product'] == product]
    plt.figure(figsize=(10, 6))
    plt.scatter(filtered_data['Count of events'], filtered_data['Amount (In Cents)'], alpha=0.5)
    plt.title(f'Relationship Between Event Counts and Revenue ({product})')
    plt.xlabel('Count of Events')
    plt.ylabel('Total Revenue (In Cents)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Print summaries
print("Product Summary:")
print(product_summary)

print("Segment Summary:")
print(segment_summary)
