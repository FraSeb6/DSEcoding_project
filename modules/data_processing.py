import pandas as pd
import pandas as pd
import streamlit as st
import geopandas as gpd
from shapely.geometry import Point
from modules.operations import *
from modules.visualization import *

# Function to load dataset based on the selected table name
def load_data(table_name):
    if table_name == "country":
        return pd.read_csv('./dataset/GlobalLandTemperaturesByCountry.csv')
    elif table_name == "city":
        return pd.read_csv('./dataset/GlobalLandTemperaturesByCity.csv')
    elif table_name == "major_city":
        return pd.read_csv('./dataset/GlobalLandTemperaturesByMajorCity.csv')
    elif table_name == "state":
        return pd.read_csv('./dataset/GlobalLandTemperaturesByState.csv')
    elif table_name == "global_temp_country":
        return pd.read_csv('./dataset/GlobalTemperatures.csv')
    else:
        return None

# Function to convert a column to datetime
def convert_to_datetype(df, column_name):
    df[column_name] = pd.to_datetime(df[column_name], errors='coerce')
    return df

# Function to get the year range from a date column
def get_year_range(df, date_column):
    """
    Get the range of years from a date column.
    
    Parameters:
    - df: DataFrame containing the data.
    - date_column: The name of the column containing the dates.
    
    Returns:
    - min_year: The first (minimum) year in the dataset.
    - max_year: The last (maximum) year, the nearest to ours days.
    """
    min_year = df[date_column].min().year
    max_year = df[date_column].max().year
    return min_year, max_year



# Function to filter data based on the selected year range
def filter_data_by_year(df, date_column, min_year, max_year):
    """
    Filters the data based on a selected year range.
    
    Parameters:
    - df: DataFrame containing the data.
    - date_column: The name of the column containing the dates.
    - min_year: The minimum year of the range.
    - max_year: The maximum year of the range.
    
    Returns:
    - df_filtered: The filtered DataFrame based on the selected year range.
    """
    # Ensure the 'date_column' is in datetime format
    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    # Filter the data based on the year range
    df_filtered = df[(df[date_column].dt.year >= min_year) & (df[date_column].dt.year <= max_year)]    
    return df_filtered


def generate_stats_df(filtered_data, place_selected, column_name, temp_column='AverageTemperature'):
    """
    Generates a DataFrame with descriptive statistics for the selected places.
    
    Parameters:
    - filtered_data: The DataFrame containing the filtered data.
    - place_selected: The list of places (cities, countries, etc.) for which the statistics are generated.
    - column_name: The column name that identifies the places (e.g., 'City').
    - temp_column: The column name containing the temperature data (default 'AverageTemperature').
    
    Returns:
    - stats_df: The DataFrame with descriptive statistics for the selected places.
    """
    
    stats_data = []
    for place in place_selected:
        # Filter the data for each place
        place_data = filtered_data[filtered_data[column_name] == place]
        
        # Calculate descriptive statistics for the place
        place_stats = descriptive_stats(place_data, temp_column)# function from operations.py
        
        # Add the name of the place to the statistics
        place_stats[column_name] = place
        
        # Add the calculated statistics to the list
        stats_data.append(place_stats)

    # Create the DataFrame with the descriptive statistics
    stats_df = pd.DataFrame(stats_data)

    # Set the 'column_name' (e.g., 'City') as the index
    stats_df.set_index(column_name, inplace=True)
    
    return stats_df


def convert_coordinate(coord):
    """
    Converts a coordinate with a direction (N/S/E/W) to a numeric format.
    
    Parameters:
    - coord: The coordinate string that may include a direction (e.g., '40.7128N', '74.0060W').
    
    Returns:
    - A float value representing the numeric coordinate, with negative values for South and West.
    """
    if 'N' in coord or 'E' in coord:
        return float(coord[:-1])  # If it's North or East, just remove the direction and convert to float
    elif 'S' in coord or 'W' in coord:
        return -float(coord[:-1])  # If it's South or West, remove the direction and make it negative
    return float(coord)  # If there is no direction, just return the float of the coordinate


def add_average_annual_temperature(df, date_column, temperature_column, temperature_column_name="Average_annual_temperature"):
    df['Year'] = df[date_column].dt.year
    avg_temp_per_city = df.groupby(['City', 'Year'])[temperature_column].mean().reset_index()
    avg_temp_per_city = avg_temp_per_city.rename(columns={temperature_column: temperature_column_name})
    df = df.merge(avg_temp_per_city, on=['City', 'Year'], how='right')
    df = df.drop(columns=['Year'])
    return df


def add_color_column_with_hex(df, temperature_column='Average_annual_temperature', colormap_name="coolwarm"):
    """
    Adds a column with HEX color values based on the temperature using the specified colormap.
    
    Parameters:
    - df: The DataFrame to which the color column is added.
    - temperature_column: The column name that contains the temperature data (default 'Average_annual_temperature').
    - colormap_name: The colormap to use for mapping temperatures to colors (default "coolwarm").
    
    Returns:
    - df: The DataFrame with the added 'Color_hex' column containing HEX color values.
    """
    # Get the colormap and normalize the temperature data
    colormap = plt.get_cmap(colormap_name)
    norm = plt.Normalize(df[temperature_column].min(), df[temperature_column].max())
    # Apply the colormap to the temperature values and convert to HEX
    df["Color_hex"] = df[temperature_column].apply(
        lambda temp: "#{:02x}{:02x}{:02x}".format(
            int(colormap(norm(temp))[0] * 255),  # Red
            int(colormap(norm(temp))[1] * 255),  # Green
            int(colormap(norm(temp))[2] * 255)   # Blue
        )
    )
    return df

def get_unique_city_data(df):
    unique_cities = df.drop_duplicates(subset=['City'])
    return unique_cities

def get_month_range(df, date_column, year):
    df_year = df[df[date_column].dt.year == year]
    min_month = df_year[date_column].min().month
    max_month = df_year[date_column].max().month
    return min_month, max_month

def filter_data_by_year_month(df, date_column, year, month):
    df_filtered = df[(df[date_column].dt.year == year) & (df[date_column].dt.month == month)]
    df_filtered = df_filtered.dropna(subset=['AverageTemperature'])
    return df_filtered

def city_selector(df, column_name, phrase, exclude_city=None):
    cities = df[column_name].unique()
    if exclude_city:
        cities = [city for city in cities if city != exclude_city]  #This line uses a list comprehension to create a new list of cities. Here's how it works:
                                                                    # city for city in cities: This part iterates over each city in the original cities list.
                                                                    #if city != exclude_city: This condition filters out any city that matches the exclude_city value.
    selected_city = st.selectbox(phrase, cities)
    return selected_city

# Function to create a GeoDataFrame with city geometries
def create_geodf(df, lat_col='Latitude', lon_col='Longitude'):
    geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
    geo_data = gpd.GeoDataFrame(df, geometry=geometry)
    return geo_data