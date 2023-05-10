import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter

# Merging the 12 months
df = pd.read_csv("Sales_Data/Sales_May_2019.csv")
files = [file for file in os.listdir('./Sales_Data')]

all_months_data = pd.DataFrame()
# concat these files to one larger file
for file in files:
    df = pd.read_csv("./Sales_Data/" + file)
    all_months_data = pd.concat([all_months_data, df])
all_data = all_months_data
# Reading the Updated full Dataframe
# print(all_months_data.head())
all_months_data.to_csv("all_data.csv", index=False)

# we add a month colomn to make it easier to read
all_data["Month"] = all_data['Order Date'].str[0:2]
# all_data["Month"] = all_data["Month"].astype('int32') # causes an error NAn
# there is NAN in our data so we need to clean it
nan_df = all_data[all_data.isna().any(axis=1)]
# print(nan_df)
all_data = all_data.dropna(how="all")
# print(all_data.head())
# all_data["Month"] = all_data["Month"].astype('int32') # Find or and delete it
all_data = all_data[all_data["Order Date"].str[0:2] != "Or"]
all_data["Month"] = all_data["Month"].astype('int32')  # Fixed
# print(all_data)

# Best month of sales ?
# we add sales column
# all_data["Sales"] = all_data["Quantity Ordered"] * all_data["Price Each"] # they look like numbers but are strings
all_data["Quantity Ordered"] = pd.to_numeric(all_data["Quantity Ordered"])  # make int
all_data["Price Each"] = pd.to_numeric(all_data["Price Each"])  # make float
all_data["Sales"] = all_data["Quantity Ordered"] * all_data["Price Each"]  # cleaned
# print(all_data.head())
results = all_data.groupby('Month').sum()  # DEC was the best in sales

# Plot the months
# months = range(1, 13)
# plt.bar(months, results['Sales'])
# plt.xticks(months)
# plt.ylabel("Sales in USD ($)")
# plt.xlabel("Month number")
# plt.show() # shows us the months and sales
# What city had the highest number of sales ?
# we add a city column .apply can be used
# def get_city(address):
#     return address.split(',')[1]
#
#
# def get_state(address):
#     return address.split(',')[2].split(' ')[1]
#
#
# all_data["City"] = all_data["Purchase Address"].apply(lambda x: get_city(x) + " " + get_state(x) + " ")
# # print(all_data.head())
# # What city had the highest number of sales ?
# results = all_data.groupby("City").sum()
# # print(results)

# Plot the City
# cities = all_data["City"].unique()  # the order between x and y is off
# cities = [city for city, df in all_data.groupby('City')]  # makes it organized
# plt.bar(cities, results['Sales'])
# plt.xticks(cities, rotation='vertical', size=8)
# plt.ylabel("Sales in USD ($)")
# plt.xlabel("US city names")
# plt.show()  # shows us the City and sales

# What time should we display advertisement to increase sales
# all_data["Order Date"] = pd.to_datetime(all_data["Order Date"])
# all_data["Hour"] = all_data["Order Date"].dt.hour
# all_data["Minutes"] = all_data["Order Date"].dt.minute
# hours = [hour for hour, df in all_data.groupby("Hour")]

# plt.plot(hours, all_data.groupby(['Hour']).count())
# plt.xticks(hours)
# plt.xlabel("Hours")
# plt.ylabel("Number of orders")
# plt.grid()
# plt.show()
# print(all_data.head())

# which Products are often sold together
df = all_data[all_data["Order ID"].duplicated(keep=False)]
df["Grouped"] = df.groupby("Order ID")["Product"].transform(lambda x: ",".join(x))
df = df[["Order ID", "Grouped"]].drop_duplicates()
# print(df.head(20))
# From StackOverflow
count = Counter()
for row in df["Grouped"]:
    row_list = row.split(",")
    count.update(Counter(combinations(row_list, 2)))
for key, value in count.most_common(10):
    print(key, value)

# What product sold the most and why?
product_group = all_data.groupby("Product")
product_group.sum()
quantity_ordered = product_group.sum()["Quantity Ordered"]
products = [product for product, df in product_group]
plt.bar(products, quantity_ordered)
plt.xticks(products, rotation="vertical", size=8)
plt.ylabel('#Ordered')
plt.xlabel('Product')
# plt.show()
# overlay the prices with the product to prove why certain items get sold more
#
# prices = all_data.groupby('Product').mean()["Price Each"]
# fig, ax1 = plt.subplots()
# ax2 = ax1.twinx()
# ax1.bar(products, quantity_ordered, color='g')
# ax2.plot(products, prices, 'b-')
#
# ax1.set_xlabel('Product Name')
# ax1.set_ylabel('Quantity Ordered', color='g')
# ax2.set_ylabel('Price ($)', color='b')
# ax1.set_xticklabels(products, rotation="vertical", size=8)
# plt.show()
