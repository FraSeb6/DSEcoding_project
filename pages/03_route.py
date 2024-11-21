import pandas as pd
import geopandas as gpd
import streamlit as st
import folium
from streamlit_folium import st_folium
from shapely.geometry import Point
from modules.data_processing import *
from modules.visualization import *
from modules.operations import *

# Set the page title
st.set_page_config(page_title="Route", layout="wide")
st.title("OPTIMAL ROUTE BETWEEN TWO CITIES")






selected_table = st.selectbox(
    "Select a table",
    ["major_city", "city"]
)
col1, col2 = st.columns(2)
selected_df = load_data(selected_table)


selected_table = convert_to_datetype(selected_df, "dt")


with col1:
    selected_year = year_monoslider()


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
st_folium(mapa, width=1200, height=800)
