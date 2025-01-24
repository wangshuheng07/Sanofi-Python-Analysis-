import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Read Excel files
file_path = "/Users/shuheng/Downloads/Product_Usage_Analysis.xlsx"
file_path2 = "/Users/shuheng/Downloads/Segmentation_Data_Export.xlsx"
product_usage = pd.read_excel(file_path)##sheet_name="Product_Usage_Analysis")
segmentation = pd.read_excel(file_path2) ##sheet_name="Segmentation_Data_Export")


print(product_usage.info())
print(product_usage.isnull().sum())


# Data cleaning
product_usage = product_usage.dropna(subset=['Count of events', 'Amount (In Cents)'])


# Data cleaning
product_usage = product_usage.dropna(subset=['Count of events', 'Amount (In Cents)'])

# Ensure 'Date' column is in datetime format
product_usage['Date'] = pd.to_datetime(product_usage['Date'], errors='coerce')


# Data merging
merged_data = product_usage.merge(segmentation, on="Merchant", how="left")

# Group by Segment
product_summary = merged_data.groupby('Product').agg(
    Total_Events=('Count of events', 'sum'),
    Total_Revenue=('Amount (In Cents)', 'sum'),
    Average_Revenue=('Amount (In Cents)', 'mean')
).reset_index()

# Set bar chart colors
segment_summary = merged_data.groupby('Segment').agg(
    Total_Events=('Count of events', 'sum'),
    Total_Revenue=('Amount (In Cents)', 'sum')
).reset_index()


# Group by overall time series
time_series_data = product_usage.groupby('Date').agg(
    Total_Revenue=('Amount (In Cents)', 'sum'),
    Total_Events=('Count of events', 'sum')
).reset_index()




# Define a function to format numbers as "X Billion"
def billions(x, pos):
    return f'{x * 1e-9:.1f}B'

# Set Y-axis format to "Billion"
formatter = FuncFormatter(billions)


# Visualization
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


# Visualization 2: Line chart for Total Revenue Over Time
plt.figure(figsize=(10, 6))
plt.plot(time_series_data['Date'], time_series_data['Total_Revenue'], marker='o', label='Total Revenue (Overall)')
plt.title('Total Revenue Over Time (Overall)')
plt.xlabel('Date')
plt.ylabel('Total Revenue')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Visualization 3: Line chart for Total Events Over Time
plt.figure(figsize=(10, 6))
plt.plot(time_series_data['Date'], time_series_data['Total_Events'], marker='o', color='orange', label='Total Events (Overall)')
plt.title('Total Events Over Time (Overall)')
plt.xlabel('Date')
plt.ylabel('Total Events')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()



# Filter specific product (e.g., Marketplaces)
filtered_data = product_usage[product_usage['Product'] == 'Marketplaces']

# Group by time series for the specific product
marketplaces_time_series = filtered_data.groupby('Date').agg(
    Total_Revenue=('Amount (In Cents)', 'sum'),
    Total_Events=('Count of events', 'sum')
).reset_index()

# Visualization 4: Line chart for Total Revenue Over Time (Marketplaces)
plt.figure(figsize=(10, 6))
plt.plot(marketplaces_time_series['Date'], marketplaces_time_series['Total_Revenue'], marker='o', color='green', label='Total Revenue (Marketplaces)')
plt.title('Total Revenue Over Time (Marketplaces)')
plt.xlabel('Date')
plt.ylabel('Total Revenue')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Visualization 5: Line chart for Total Events Over Time (Marketplaces)
plt.figure(figsize=(10, 6))
plt.plot(marketplaces_time_series['Date'], marketplaces_time_series['Total_Events'], marker='o', color='red', label='Total Events (Marketplaces)')
plt.title('Total Events Over Time (Marketplaces)')
plt.xlabel('Date')
plt.ylabel('Total Events')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# Repeat the same process for other products: Cart, Recurring, and Basic API

# Filter specific product (Cart)
filtered_data_cart = product_usage[product_usage['Product'] == 'Cart']

# Group by time series for Cart
cart_time_series = filtered_data_cart.groupby('Date').agg(
    Total_Revenue=('Amount (In Cents)', 'sum'),
    Total_Events=('Count of events', 'sum')
).reset_index()

# Visualization 6: Total Revenue Over Time (Cart)
plt.figure(figsize=(10, 6))
plt.plot(cart_time_series['Date'], cart_time_series['Total_Revenue'], marker='o', color='purple', label='Total Revenue (Cart)')
plt.title('Total Revenue Over Time (Cart)')
plt.xlabel('Date')
plt.ylabel('Total Revenue')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Visualization 7: Total Events Over Time (Cart)
plt.figure(figsize=(10, 6))
plt.plot(cart_time_series['Date'], cart_time_series['Total_Events'], marker='o', color='blue', label='Total Events (Cart)')
plt.title('Total Events Over Time (Cart)')
plt.xlabel('Date')
plt.ylabel('Total Events')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Filter specific product (Recurring)
filtered_data_recurring = product_usage[product_usage['Product'] == 'Recurring']

# Group by time series for Recurring
recurring_time_series = filtered_data_recurring.groupby('Date').agg(
    Total_Revenue=('Amount (In Cents)', 'sum'),
    Total_Events=('Count of events', 'sum')
).reset_index()

# Visualization 8: Total Revenue Over Time (Recurring)
plt.figure(figsize=(10, 6))
plt.plot(recurring_time_series['Date'], recurring_time_series['Total_Revenue'], marker='o', color='orange', label='Total Revenue (Recurring)')
plt.title('Total Revenue Over Time (Recurring)')
plt.xlabel('Date')
plt.ylabel('Total Revenue')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Visualization 9: Total Events Over Time (Recurring)
plt.figure(figsize=(10, 6))
plt.plot(recurring_time_series['Date'], recurring_time_series['Total_Events'], marker='o', color='brown', label='Total Events (Recurring)')
plt.title('Total Events Over Time (Recurring)')
plt.xlabel('Date')
plt.ylabel('Total Events')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Filter specific product (Basic API)
filtered_data_basic_api = product_usage[product_usage['Product'] == 'Basic API']

# Group by time series for Basic API
basic_api_time_series = filtered_data_basic_api.groupby('Date').agg(
    Total_Revenue=('Amount (In Cents)', 'sum'),
    Total_Events=('Count of events', 'sum')
).reset_index()

# Visualization 10: Total Revenue Over Time (Basic API)
plt.figure(figsize=(10, 6))
plt.plot(basic_api_time_series['Date'], basic_api_time_series['Total_Revenue'], marker='o', color='cyan', label='Total Revenue (Basic API)')
plt.title('Total Revenue Over Time (Basic API)')
plt.xlabel('Date')
plt.ylabel('Total Revenue')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Visualization 11: Total Events Over Time (Basic API)
plt.figure(figsize=(10, 6))
plt.plot(basic_api_time_series['Date'], basic_api_time_series['Total_Events'], marker='o', color='pink', label='Total Events (Basic API)')
plt.title('Total Events Over Time (Basic API)')
plt.xlabel('Date')
plt.ylabel('Total Events')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# Scatter plot for Count of Events vs Total Revenue (Overall)
plt.figure(figsize=(10, 6))
plt.scatter(product_usage['Count of events'], product_usage['Amount (In Cents)'], alpha=0.5, c='blue')
plt.title('Relationship Between Event Counts and Revenue (Overall)')
plt.xlabel('Count of Events')
plt.ylabel('Total Revenue (In Cents)')
plt.grid(True)
plt.tight_layout()
plt.show()

# Scatter plot for each product (e.g., Marketplaces)
for product in product_usage['Product'].unique():
    filtered_data = product_usage[product_usage['Product'] == product]
    plt.figure(figsize=(10, 6))
    plt.scatter(filtered_data['Count of events'], filtered_data['Amount (In Cents)'], alpha=0.5)
    plt.title(f'Relationship Between Event Counts and Revenue ({product})')
    plt.xlabel('Count of Events')
    plt.ylabel('Total Revenue (In Cents)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# Print summary
print("Product Summary:")
print(product_summary)

print("Segment Summary:")
print(segment_summary)
