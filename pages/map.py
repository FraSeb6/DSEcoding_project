import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
import streamlit as st
from streamlit_folium import st_folium

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

# Function to add markers to the map (excluding rows with NaN temperature)
def create_map_with_markers(df):
    # Filter out rows where Average_annual_temperature is NaN
    df = df.dropna(subset=['Average_annual_temperature'])#I noticed that, there was some point where the temperature was not available

    # Create the map centered on the mean latitude and longitude of the cities
    m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=2)

    # Add a marker for each city
    for _, column in df.iterrows():
        popup_text = f"""
        <b>City:</b> {column['City']}<br>
        <b>Country:</b> {column['Country']}<br>
        <b>Temperature:</b> {column['Average_annual_temperature']}°C<br>
        <b>Coordinates:</b> ({column['Latitude']}, {column['Longitude']})
        """
        folium.CircleMarker(
            location=[column['Latitude'], column['Longitude']],
            radius=8,
            color=column['Color_hex'],
            fill=True,
            fill_color=column['Color_hex'],
            fill_opacity=0.8,
            popup=folium.Popup(popup_text, max_width=200)
        ).add_to(m)  # Add the marker to the map

    return m  # Return the map created

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
selected_year = year_slider(min_year, max_year)

# Filter the data by the selected year
dataframe_filtered_by_year = filter_data_by_year(dataframe_selected, "dt", selected_year)

# Add the average annual temperature to the filtered data
dataframe_filtered_by_year = add_average_annual_temperature(dataframe_filtered_by_year, "dt", "AverageTemperature")

# Convert latitude and longitude to numeric coordinates
dataframe_filtered_by_year = convert_coordinates(dataframe_filtered_by_year, "Latitude", "Longitude")
dataframe_filtered_by_year = conveart_corrdinates_floattype(dataframe_filtered_by_year, "Latitude", "Longitude")

# Add a color column based on the average annual temperature
dataframe_filtered_by_year = add_color_column(dataframe_filtered_by_year)

# Convert RGBA to hex color format
dataframe_filtered_by_year['Color_hex'] = dataframe_filtered_by_year['Color'].apply(rgba_to_hex)

# Get unique city data (removes duplicates)
dataframe_filtered_by_year = get_unique_city_data(dataframe_filtered_by_year)



# Create the map with the markers
map_with_markers = create_map_with_markers(dataframe_filtered_by_year)

# Display the map
st_folium(map_with_markers, width=700, height=500)

# Disclaimer note
st.write(":red[DISCLAIMER: The coordinates are not accurate.]")
