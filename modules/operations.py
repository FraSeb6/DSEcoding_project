import numpy as np
import pandas as pd
import streamlit as st


def descriptive_stats(data, temp_column):
    """
    Calculates descriptive statistics for a temperature column in a DataFrame.
    Also adds the temperature range (max - min).

    Parameters:
    - data: DataFrame containing the data.
    - temp_column: The name of the column containing the temperatures.

    Returns:
    - stats: Dictionary containing the descriptive statistics (min, max, mean, median, std, range).
    """
    # Remove NaN values
    temperatures = data[temp_column].dropna()

    # Calculate descriptive statistics
    stats = {
        "Min": np.min(temperatures), # Minimum temperature
        "Max": np.max(temperatures), # Maximum temperature
        "Range": np.max(temperatures) - np.min(temperatures), # Temperature range
        "Mean": np.mean(temperatures), # Mean temperature
        "Q1": np.percentile(temperatures, 25), # First quartile
        "Median": np.median(temperatures), # Median temperature
        "Q3": np.percentile(temperatures, 75),  # Third quartile
        "Std Dev": np.std(temperatures), # Standard deviation
        "IQR": np.percentile(temperatures, 75) - np.percentile(temperatures, 25), # Interquartile range
        "Number of Observations": len(temperatures), # Number of observations
        "Variance": np.var(temperatures), # Variance
        "Coefficient of Variation": np.std(temperatures) / np.mean(temperatures), # Coefficient of variation
    }

    return stats

def multieselector_place(data, column_name, default_place=['New York', 'Los Angeles']):
    """
    Returns the list of cities selected by the user in the multiselect.
    If the user does not select any cities, it returns the two default cities.

    Parameters:
    - data: DataFrame containing the city data.
    - default_place: List of two default cities (default 'New York' and 'Los Angeles').

    Returns:
    - place_selected: List of cities selected by the user.
    """
    # Multiselect for selecting cities, with two default cities
    place_selected = st.multiselect(
        "Select the cities",
        options=data[column_name].unique(),
        default=default_place  # Set two default cities
    )

    # If no cities are selected, use the default cities
    if len(place_selected) == 0:
        st.warning("Please select at least one city.")  # Show a warning if no city is selected
        place_selected = default_place  # If no cities are selected, replace with default cities

    return place_selected


def year_slider(min_year, max_year):
    """
    Creates a slider to select a range of years.
    
    Parameters:
    - min_year: The minimum year.
    - max_year: The maximum year.
    
    Returns:
    - selected_year_range: The selected year range from the slider.
    """
    selected_year_range = st.slider(
        "Select a range of years",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1  # Set the step value to 1
    )
    return selected_year_range


def year_monoslider(min_year=1760, max_year=2011):
    selected_year = st.slider(
        "Select a year",
        min_value=min_year,
        max_value=max_year,
        value=2002
    )
    return selected_year

def get_month_range(df, date_column, year):
    df_year = df[df[date_column].dt.year == year]
    min_month = df_year[date_column].min().month
    max_month = df_year[date_column].max().month
    return min_month, max_month

def month_slider(min_month, max_month):
    selected_month = st.slider(
        "Select a month",
        min_value=min_month,
        max_value=max_month,
        value=9
    )
    return selected_month

def find_path(geo_data, start_city, end_city, w_T=0.4, w_D=0.6):
    """
    Finds the optimal path between two cities based on a score that combines
    average temperature and distance to the destination.
    """
    # Find the start and end points
    start = geo_data[geo_data['City'] == start_city]
    end = geo_data[geo_data['City'] == end_city]

    if start.empty or end.empty:
        raise ValueError("One of the specified cities is not in the dataset.")

    # Initialize the path and current point
    path = [start_city]
    current = start

    while current['City'].values[0] != end_city:
        # Calculate the distance from all cities that have not been visited yet
        remaining = geo_data[~geo_data['City'].isin(path)]

        # Calculate the distance from the current point
        remaining['distance_from_current'] = remaining.geometry.distance(current.geometry.values[0])

        # Select the three closest cities
        closest = remaining.nsmallest(3, 'distance_from_current')

        # Check if the destination city is among the closest cities
        if end_city in closest['City'].values:
            path.append(end_city)
            break

        # Calculate the distance to the destination for the score
        closest['distance_to_dest'] = closest.geometry.distance(end.geometry.values[0])

        # Calculate the combined score
        closest['score'] = (
            w_T * closest['AverageTemperature'] - w_D * closest['distance_to_dest']
        )

        # Choose the city with the highest score
        next_city = closest.loc[closest['score'].idxmax()]

        # Add the selected city to the path
        path.append(next_city['City'])
        current = geo_data[geo_data['City'] == next_city['City']]
    return path



