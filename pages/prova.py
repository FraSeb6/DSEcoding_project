import pandas as pd

# Load your dataset
df = pd.read_csv('path_to_your_dataset.csv')

# Replace 'major_city' and 'temperature' with the actual column names in your dataset
major_cities = df['major_city'].unique()

# Dictionary to store years without temperature values for each city
years_without_temp = {}

for city in major_cities:
    city_data = df[df['major_city'] == city]
    years_with_temp = city_data.dropna(subset=['temperature'])['year'].unique()
    all_years = city_data['year'].unique()
    years_without_temp[city] = [year for year in all_years if year not in years_with_temp]

# Print the results
for city, years in years_without_temp.items():
    print(f"{city}: {years}")