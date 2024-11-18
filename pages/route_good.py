import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from shapely.geometry import Point

@st.cache_data




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

def convert_to_date(df, column_name):
    df[column_name] = pd.to_datetime(df[column_name], errors='coerce')
    return df

def get_year_range(df, date_column):
    min_year = df[date_column].min().year
    max_year = df[date_column].max().year
    return min_year, max_year

def year_slider(min_year, max_year):
    selected_year = st.slider(
        "Select a year",
        min_value=min_year,
        max_value=max_year,
        value=min_year
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
        value=min_month
    )
    return selected_month

def filter_data_by_year_month(df, date_column, year, month):
    df_filtered = df[(df[date_column].dt.year == year) & (df[date_column].dt.month == month)]
    return df_filtered


def city_selector(df, column_name, phrase, exclude_city=None):
    cities = df[column_name].unique()
    if exclude_city:
        cities = [city for city in cities if city != exclude_city]  #This line uses a list comprehension to create a new list of cities. Here's how it works:
                                                                    # city for city in cities: This part iterates over each city in the original cities list.
                                                                    #if city != exclude_city: This condition filters out any city that matches the exclude_city value.
    selected_city = st.selectbox(phrase, cities)
    return selected_city

def convert_coordinate(coord):
    if 'N' in coord or 'E' in coord:
        return float(coord[:-1])
    elif 'S' in coord or 'W' in coord:
        return -float(coord[:-1])
    return float(coord)


# Funzione per creare un GeoDataFrame con le geometrie delle città
def create_geodf(df, lat_col='Latitude', lon_col='Longitude'):
    geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
    geo_data = gpd.GeoDataFrame(df, geometry=geometry)
    return geo_data

def find_optimized_path(geo_data, start_city, end_city, w_T=0.1, w_D=0.9):
    # Trova i punti di partenza e arrivo
    start = geo_data[geo_data['City'] == start_city]
    end = geo_data[geo_data['City'] == end_city]

    if start.empty or end.empty:
        raise ValueError("Una delle città specificate non è nel dataset.")

    # Inizializza il percorso e il punto corrente
    path = [start_city]
    current = start

    while current['City'].values[0] != end_city:
        # Calcola la distanza da tutte le città non ancora visitate
        remaining = geo_data[~geo_data['City'].isin(path)]
        remaining['distance_from_current'] = remaining.geometry.distance(current.geometry.values[0])

        # Seleziona le tre città più vicine
        closest = remaining.nsmallest(3, 'distance_from_current')

        # Controlla se la città di destinazione è tra le più vicine
        if end_city in closest['City'].values:
            path.append(end_city)
            break

        # Calcola la distanza dalla destinazione per il punteggio
        closest['distance_to_dest'] = closest.geometry.distance(end.geometry.values[0])

        # Calcola il punteggio combinato
        closest['score'] = (
            w_T * closest['AverageTemperature'] - w_D * closest['distance_to_dest']
        )

        # Scegli la città con il punteggio più alto
        next_city = closest.loc[closest['score'].idxmax()]

        # Aggiungi la città scelta al percorso
        path.append(next_city['City'])
        current = geo_data[geo_data['City'] == next_city['City']]

    return path










selected_table = st.selectbox(
    "Select a table",
    ["major_city", "city"]
)

selected_df = load_data(selected_table)

selected_table = convert_to_date(selected_df, "dt")

min_year, max_year = get_year_range(selected_df, "dt")

selected_year = year_slider(min_year, max_year)

min_month, max_month = get_month_range(selected_df, "dt", selected_year)

selected_month = month_slider(min_month, max_month)

filtered_df = filter_data_by_year_month(selected_df, "dt", selected_year, selected_month)

filtered_df = filtered_df.dropna(subset=['Latitude', 'Longitude'])
filtered_df['Latitude'] = filtered_df['Latitude'].apply(convert_coordinate)
filtered_df['Longitude'] = filtered_df['Longitude'].apply(convert_coordinate)

filtered_df = create_geodf(filtered_df, 'Latitude', 'Longitude')

start = city_selector(filtered_df, 'City', "select the start city")
arrive = city_selector(filtered_df, 'City', "select the arrive city", start)



path= find_optimized_path(filtered_df, start, arrive)

st.write(path)
st.write(filtered_df)
st.write(filtered_df.dtypes)

# Create a map centered at the midpoint of the path
midpoint = filtered_df[filtered_df['City'].isin(path)].geometry.unary_union.centroid
m = folium.Map(location=[midpoint.y, midpoint.x], zoom_start=5)
# Add markers for each city in the path
for city in path:
    city_data = filtered_df[filtered_df['City'] == city]
    folium.Marker(
        location=[city_data.geometry.y.values[0], city_data.geometry.x.values[0]],
        popup=city,
        icon=folium.Icon(color='blue')
    ).add_to(m)
    # Add lines connecting the cities in the path
    for i in range(len(path) - 1):
        city_data_1 = filtered_df[filtered_df['City'] == path[i]]
        city_data_2 = filtered_df[filtered_df['City'] == path[i + 1]]
        folium.PolyLine(
            locations=[
                [city_data_1.geometry.y.values[0], city_data_1.geometry.x.values[0]],
                [city_data_2.geometry.y.values[0], city_data_2.geometry.x.values[0]]
            ],
            color='red',
            weight=2.5,
            opacity=1
        ).add_to(m)
        # Add markers for all other cities not in the path with low opacity
        for city in filtered_df['City'].unique():
            if city not in path:
                city_data = filtered_df[filtered_df['City'] == city]
                folium.CircleMarker(
                    location=[city_data.geometry.y.values[0], city_data.geometry.x.values[0]],
                    radius=3,
                    color='gray',
                    fill=True,
                    fill_color='gray',
                    fill_opacity=0.2,
                    opacity=0.2
                ).add_to(m)
# Display the map in Streamlit
st_folium(m, width=700, height=500)