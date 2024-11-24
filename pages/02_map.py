import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_folium import st_folium
from modules.data_processing import *
from modules.operations import *
from modules.visualization import *

# Set the page title
st.set_page_config(page_title="Map", layout="wide")
st.title("MAP OF GLOBAL TEMPERATURE DATA")

# Streamlit app interface
selected_table = st.selectbox(
    "Select a table",
    ["major_city", "city"]
)

st.write(f"Displaying data from {selected_table} table")

# Load the dataset
dataframe_selected = load_data(selected_table)

# Convert 'dt' column to datetime
dataframe_selected = convert_to_datetype(dataframe_selected, "dt")

# Get the range of years from the dataset
min_year, max_year = get_year_range(dataframe_selected, "dt")

# Year slider to select the desired year
selected_year = year_monoslider(min_year, max_year)

# Filter the data by the selected year
dataframe_filtered_by_year = filter_data_by_oneyear(dataframe_selected, "dt", selected_year)

# Add the average annual temperature to the filtered data
dataframe_filtered_by_year = add_average_annual_temperature(dataframe_filtered_by_year, "dt", "AverageTemperature")

# Convert latitude and longitude to numeric coordinates
dataframe_filtered_by_year = dataframe_filtered_by_year.dropna(subset=['Latitude', 'Longitude'])
dataframe_filtered_by_year['Latitude'] = dataframe_filtered_by_year['Latitude'].apply(convert_coordinate)
dataframe_filtered_by_year['Longitude'] = dataframe_filtered_by_year['Longitude'].apply(convert_coordinate)


dataframe_filtered_by_year = add_color_column_with_hex(dataframe_filtered_by_year)
# Get unique city data (removes duplicates)
dataframe_filtered_by_year = get_unique_city_data(dataframe_filtered_by_year)



# Create the map with the markers
display_map(dataframe_filtered_by_year)



# Disclaimer note
st.write(":red[DISCLAIMER: The coordinates are not accurate.]")
