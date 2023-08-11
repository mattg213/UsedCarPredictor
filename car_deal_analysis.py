import pandas as pd
import csv 
# Assume data is loaded and processed here, replace with actual loading code
data = pd.read_csv('cleaned.csv',low_memory=False)

# Grouping by the relevant features and calculating the mean price for each group
columns_to_group_by = ['make_name', 'model_name', 'year']
grouped_data = data.groupby(columns_to_group_by)['price'].mean().reset_index()

def determine_deal(make_name, model_name, year, user_price):
    group = grouped_data[
        (grouped_data['make_name'] == make_name) &
        (grouped_data['model_name'] == model_name) &
        (grouped_data['year'] == year)   
    ]

    if len(group.index) == 0:
        return "No similar cars found in data"

    mean_price = group['price'].iloc[0]  # Removed .compute() assuming using pandas

    if user_price < mean_price:
        return "Good Deal"
    else:
        return "Bad Deal"
