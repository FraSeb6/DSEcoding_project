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

# Funzione per ottenere l'intervallo degli anni da una colonna di date
def get_year_range(df, date_column):
    """
    Ottieni l'intervallo di anni da una colonna di date.
    
    Parameters:
    - df: DataFrame contenente i dati.
    - date_column: Il nome della colonna contenente le date.
    
    Returns:
    - min_year: Il primo anno (minimo).
    - max_year: L'ultimo anno (massimo).
    """
    min_year = df[date_column].min().year
    max_year = df[date_column].max().year
    return min_year, max_year



# Funzione per filtrare i dati in base all'anno selezionato
def filter_data_by_year(df, date_column, min_year, max_year):
    """
    Filtra i dati in base a un intervallo di anni selezionato.
    
    Parameters:
    - df: DataFrame contenente i dati.
    - date_column: Il nome della colonna contenente le date.
    - min_year: L'anno minimo dell'intervallo.
    - max_year: L'anno massimo dell'intervallo.
    
    Returns:
    - df_filtered: Il DataFrame filtrato per l'intervallo di anni selezionato.
    """
    # Assicurati che la colonna 'date_column' sia in formato datetime
    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    
    # Filtra i dati in base all'intervallo di anni
    df_filtered = df[(df[date_column].dt.year >= min_year) & (df[date_column].dt.year <= max_year)]
    
    return df_filtered

def generate_stats_df(filtered_data, place_selected, column_name, temp_column='AverageTemperature'):
            
    stats_data = []
    for city in place_selected:
        # Filtra i dati per ogni città
        city_data = filtered_data[filtered_data[column_name] == city]
        
        # Calcola le statistiche descrittive per la città
        city_stats = descriptive_stats(city_data, temp_column)
        
        # Aggiungi il nome della città alle statistiche
        city_stats[column_name] = city
        
        # Aggiungi le statistiche calcolate alla lista
        stats_data.append(city_stats)

    # Crea il DataFrame delle statistiche descrittive
    stats_df = pd.DataFrame(stats_data)

    # Imposta la colonna column_name come indice
    stats_df.set_index(column_name, inplace=True)
    
    return stats_df

def convert_coordinate(coord):
    if 'N' in coord or 'E' in coord:
        return float(coord[:-1])
    elif 'S' in coord or 'W' in coord:
        return -float(coord[:-1])
    return float(coord)

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