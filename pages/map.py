import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster


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

def convert_to_datetype(df, column_name):
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

def filter_data_by_year(df, date_column, year):
    df_filtered = df[df[date_column].dt.year == year]
    return df_filtered

def add_average_annual_temperature(df, date_column, temperature_column, temperature_column_name="Average_annual_temperature"):
    df['Year'] = df[date_column].dt.year
    avg_temp_per_city = df.groupby(['City', 'Year'])[temperature_column].mean().reset_index()
    avg_temp_per_city = avg_temp_per_city.rename(columns={temperature_column: temperature_column_name})
    df = df.merge(avg_temp_per_city, on=['City', 'Year'], how='right')
    df = df.drop(columns=['Year'])
    return df

def convert_coordinates(df, lat_column, lon_column):
    def convert_lat(lat):
        if 'N' in lat:
            return str(float(lat.replace('N', '')))
        elif 'S' in lat:
            return str(-float(lat.replace('S', '')))
        return None

    def convert_lon(lon):
        if 'E' in lon:
            return str(float(lon.replace('E', '')))
        elif 'W' in lon:
            return str(-float(lon.replace('W', '')))
        return None

    df[lat_column] = df[lat_column].apply(convert_lat)
    df[lon_column] = df[lon_column].apply(convert_lon)
    return df

def conveart_corrdinates_floattype(df, lat_column, lon_column):
    df[lat_column] = pd.to_numeric(df[lat_column], errors='coerce')
    df[lon_column] = pd.to_numeric(df[lon_column], errors='coerce')
    return df


def add_color_column(df, temperature_column='Average_annual_temperature', colormap_name="coolwarm"):
    colormap = plt.get_cmap(colormap_name)
    norm = plt.Normalize(df[temperature_column].min(), df[temperature_column].max())
    df["Color"] = df[temperature_column].apply(lambda temp: colormap(norm(temp)))
    return df

def rgba_to_hex(rgba):
    r, g, b, a = rgba
    return "#{:02x}{:02x}{:02x}".format(int(r*255), int(g*255), int(b*255))

def get_unique_city_data(df):
    unique_cities = df.drop_duplicates(subset=['City'])
    return unique_cities



selected_table = st.selectbox(
    "Select a table",
    ["major_city", "city"]
)

st.write(f"Displaying data from {selected_table} table")

dataframe_selected= load_data(selected_table)

dataframe_selected = convert_to_datetype(dataframe_selected, "dt")

min_year, max_year = get_year_range(dataframe_selected, "dt")

selected_year = year_slider(min_year, max_year)

dataframe_filtered_by_year = filter_data_by_year(dataframe_selected, "dt", selected_year)

dataframe_filtered_by_year = add_average_annual_temperature(dataframe_filtered_by_year, "dt", "AverageTemperature")

dataframe_filtered_by_year = convert_coordinates(dataframe_filtered_by_year, "Latitude", "Longitude")

#da inserire nelle rispettive funzioni 
dataframe_filtered_by_year = conveart_corrdinates_floattype(dataframe_filtered_by_year, "Latitude", "Longitude")

dataframe_filtered_by_year = add_color_column(dataframe_filtered_by_year)

dataframe_filtered_by_year['Color_hex'] = dataframe_filtered_by_year['Color'].apply(rgba_to_hex)

dataframe_filtered_by_year = get_unique_city_data(dataframe_filtered_by_year)



st.write("Data types of each column:")
st.write(dataframe_filtered_by_year.dtypes)
print(dataframe_selected.dtypes)
st.write(dataframe_filtered_by_year)


m = folium.Map(location=[dataframe_filtered_by_year['Latitude'].mean(), dataframe_filtered_by_year['Longitude'].mean()], zoom_start=2)

# Aggiungi un cluster di marker
#    marker_cluster = MarkerCluster().add_to(m)


#save the date in cache to avoid to reload the data every time


for _, column in dataframe_filtered_by_year.iterrows():
    #create a pop up text
    popup_text = f"""
    <b>City:</b> {column['City']}<br>
    <b>Country:</b> {column['Country']}<br>
    <b>Temperature:</b> {column['Average_annual_temperature']}°C<br>
    <b>Coordinates:</b> ({column['Latitude']}, {column['Longitude']})
    """
    #add a marker to the map
    folium.CircleMarker(
        location=[column['Latitude'], column['Longitude']],
        radius=8,
        color=column['Color_hex'],
        fill=True,
        fill_color=column['Color_hex'],
        fill_opacity=0.8,
        popup=folium.Popup(popup_text, max_width=200)
    ).add_to(m) #add the marker to the cluster |     m or marker_cluster
    
#add the layer control
st_folium(m, width=700, height=500)

st.write(":red[DISCLAIMER: the coordinates are not accurate].")

# Rimozione delle righe con valori mancanti in AverageTemperature
#clean_data = data.dropna(subset=['AverageTemperature']).copy()







