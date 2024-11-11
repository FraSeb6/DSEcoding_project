import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster



from math import radians, sin, cos, sqrt, atan2


def load_data(table_name):
    if table_name == "country":
        return pd.read_csv('.\\dataset\\GlobalLandTemperaturesByCountry.csv')
    elif table_name == "city":
        return pd.read_csv('.\\dataset\\GlobalLandTemperaturesByCity.csv')
    elif table_name == "major_city":
        return pd.read_csv('.\\dataset\\GlobalLandTemperaturesByMajorCity.csv')
    elif table_name == "state":
        return pd.read_csv('.\\dataset\\GlobalLandTemperaturesByState.csv')
    elif table_name == "global_temp_country":
        return pd.read_csv('.\\dataset\\GlobalTemperatures.csv')
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



