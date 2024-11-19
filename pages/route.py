import pandas as pd
import geopandas as gpd
import streamlit as st
import folium
from streamlit_folium import st_folium
from shapely.geometry import Point






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

def year_slider(min_year=1751, max_year=2011):
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

# maybe i can use the function wed angles to calculate the distance between two cities

def find_path(geo_data, start_city, end_city, w_T=0.4, w_D=0.6):
    """
    Trova il percorso ottimale tra due città basandosi su un punteggio che combina
    la temperatura media e la distanza dalla destinazione.
    """
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

        # Calcola la distanza dal punto corrente
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


def visualize_path(geo_data, path, start_city, end_city):
    """
    Visualizza il percorso calcolato su una mappa Folium.
    - Le città del percorso sono evidenziate e collegate da una linea.
    - Le città non visitate sono mostrate con opacità minore e includono la temperatura nel popup.
    """
    # Crea una mappa centrata sulla città di partenza
    start_coords = geo_data[geo_data['City'] == start_city].geometry.values[0]
    m = folium.Map(location=[start_coords.y, start_coords.x], zoom_start=3)

    # Aggiungi tutte le città con bassa opacità e mostra la temperatura nel popup
    for _, row in geo_data.iterrows():
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=4,
            color="gray",
            fill=True,
            fill_color="gray",
            fill_opacity=0.3,
            popup=f"{row['City']}<br>Temp: {row['AverageTemperature']:.2f}°C",
        ).add_to(m)

    # Evidenzia le città del percorso
    for city in path:
        city_data = geo_data[geo_data['City'] == city]
        city_coords = city_data.geometry.values[0]
        temperature = city_data['AverageTemperature'].values[0]
        folium.CircleMarker(
            location=[city_coords.y, city_coords.x],
            radius=6,
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.6,
            popup=f"{city}<br>Temp: {temperature:.2f}°C",
        ).add_to(m)

    # Collega le città del percorso con una linea
    path_coords = [
        [geo_data[geo_data['City'] == city].geometry.y.values[0],
         geo_data[geo_data['City'] == city].geometry.x.values[0]]
        for city in path
    ]
    folium.PolyLine(path_coords, color="blue", weight=2.5, opacity=0.6).add_to(m)

    # Evidenzia la città di partenza in verde e quella di arrivo in rosso
    start_data = geo_data[geo_data['City'] == start_city]
    start_coords = start_data.geometry.values[0]
    start_temp = start_data['AverageTemperature'].values[0]
    folium.CircleMarker(
        location=[start_coords.y, start_coords.x],
        radius=8,
        color="green",
        fill=True,
        fill_color="green",
        fill_opacity=1,
        popup=f"Partenza: {start_city}<br>Temp: {start_temp:.2f}°C",
    ).add_to(m)

    end_data = geo_data[geo_data['City'] == end_city]
    end_coords = end_data.geometry.values[0]
    end_temp = end_data['AverageTemperature'].values[0]
    folium.CircleMarker(
        location=[end_coords.y, end_coords.x],
        radius=8,
        color="red",
        fill=True,
        fill_color="red",
        fill_opacity=1,
        popup=f"Arrivo: {end_city}<br>Temp: {end_temp:.2f}°C",
    ).add_to(m)

    return m








selected_table = st.selectbox(
    "Select a table",
    ["major_city", "city"]
)
col1, col2 = st.columns(2)
selected_df = load_data(selected_table)


selected_table = convert_to_date(selected_df, "dt")


with col1:
    selected_year = year_slider()


min_month, max_month = get_month_range(selected_table, "dt", selected_year)
with col2:
    selected_month = month_slider(min_month, max_month)

filtered_df = filter_data_by_year_month(selected_table, "dt", selected_year, selected_month)

filtered_df = filtered_df.dropna(subset=['Latitude', 'Longitude'])
filtered_df['Latitude'] = filtered_df['Latitude'].apply(convert_coordinate)
filtered_df['Longitude'] = filtered_df['Longitude'].apply(convert_coordinate)

filtered_df = create_geodf(filtered_df, 'Latitude', 'Longitude')

with col1:
    start = city_selector(filtered_df, 'City', "select the start city")

with col2:
    arrive = city_selector(filtered_df, 'City', "select the arrive city", start)


path= find_path(filtered_df, start, arrive)






st.header("Map of the optimal path")
mapa = visualize_path(filtered_df, path, start, arrive)
st_folium(mapa, width=800, height=600)
