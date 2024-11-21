import streamlit as st
import pandas as pd
from modules.data_processing import *

# Set the page title
st.set_page_config(page_title="Global Temperature Data Analysis", layout="wide")

# Introduction to the project
st.title("Welcome to the Global Temperature Data Analysis Project")
st.markdown("""
    This project allows you to explore temperature data for various global regions, including cities, countries, and states.
    The data spans multiple years, and you can filter the data based on the year and region of interest.
    
    Use the **dataset selection** in the sidebar to choose which dataset to analyze. 
    Once selected, use the **year slider** to choose the specific year you want to view.
""")

# Sidebar for dataset selection
dataset_option = st.sidebar.radio(
    "Select a dataset to explore:",
    options=["city", "major_city", "state", "country", "global_temp_country"]
)

# Load the selected dataset
st.write(f"Displaying data from the **{dataset_option}** dataset")
data = load_data(dataset_option)
data = data.dropna()
data = convert_to_datetype(data, 'dt')
col1, col2 = st.columns([3,1])
if data is not None:
    # Show the first few rows of the selected dataset
    st.write("### Dataset Preview:")
    with col1:
        st.write(data)
    with col2:
        st.write(data.dtypes)

    # Get the year range for the dataset
    min_year, max_year = get_year_range(data, 'dt')
    
    # Slider to select the year
    selected_year = year_slider(min_year, max_year)
    st.write(f"### Data for the year {selected_year}:")
    
    # Filter the data based on the selected year
    data_filtered_by_year = data[data['dt'].dt.year == selected_year]
    
    # Show filtered data for the selected year
    st.write(data_filtered_by_year)

else:
    st.write("### Error: Unable to load the selected dataset.")
