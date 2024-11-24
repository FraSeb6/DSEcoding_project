import streamlit as st
import pandas as pd
from modules.data_processing import *
from modules.visualization import *
from modules.operations import *

# Set the page title
st.set_page_config(page_title="Dataset Table", layout="wide")
st.title("TABLE OF GLOBAL TEMPERATURE DATA")

# Load the dataset of cities
dataset_option = st.sidebar.radio(
    "Select a dataset to display",
    options=["major_city", "state", "country", "city"]
)

# Load the dataset
data = load_data(dataset_option)

if dataset_option == "major_city" or dataset_option == "city":
    st.write(f"Dataset: {dataset_option}")
    
    # Convert the 'dt' column to datetime format
    data = convert_to_datetype(data, 'dt')

    # Get the year range
    min_year, max_year = get_year_range(data, 'dt')

    # Get the list of selected cities, with the two default cities
    cities_selected = multieselector_place(data, 'City', default_place=['New York', 'Los Angeles'])

    # Filter the data based on the selected cities
    filtered_data_for_desc = filter_data_by_year(data, 'dt', min_year, max_year)
    filtered_data_for_desc = filtered_data_for_desc[filtered_data_for_desc['City'].isin(cities_selected)]

    # Calculate descriptive statistics for the selected cities
    stats_df = generate_stats_df(filtered_data_for_desc, cities_selected, 'City', 'AverageTemperature')

    # Display the descriptive statistics table with city names as the index
    st.write("Descriptive Statistics of Temperatures for Selected Cities:")
    st.dataframe(stats_df)

    # Range slider to select a range of years
    selected_year_range = year_slider(min_year, max_year)

    # Filter the data based on the selected year range
    filtered_data = filter_data_by_year(data, 'dt', selected_year_range[0], selected_year_range[1])

    # Display the chart based on the selection
    display_chart(filtered_data, place_selected=cities_selected, place_column='City', temp_column='AverageTemperature')

elif dataset_option == "state" or dataset_option == "country":
    st.write(f"Dataset: {dataset_option}")
    
    # Convert the 'dt' column to datetime format
    data = convert_to_datetype(data, 'dt')

    # Get the year range
    min_year, max_year = get_year_range(data, 'dt')

    # Get the list of selected countries, with the two default countries
    countries_selected = multieselector_place(data, 'Country', default_place=['United States', 'Canada'])

    # Filter the data based on the selected countries
    filtered_data = filter_data_by_year(data, 'dt', min_year, max_year)
    filtered_data = filtered_data[filtered_data['Country'].isin(countries_selected)]

    # Calculate descriptive statistics for the selected countries
    stats_df = generate_stats_df(filtered_data, countries_selected, 'Country')

    # Display the descriptive statistics table with country names as the index
    st.write("Descriptive Statistics of Temperatures for Selected Countries:")
    st.dataframe(stats_df)

    # Range slider to select a range of years
    selected_year_range = year_slider(min_year, max_year)

    # Filter the data based on the selected year range
    filtered_data = filter_data_by_year(data, 'dt', selected_year_range[0], selected_year_range[1])

    # Display the chart based on the selection
    display_chart(filtered_data, place_selected=countries_selected, place_column='Country', temp_column='AverageTemperature')

else:
    st.write("Invalid or missing dataset.")
