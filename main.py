
import pandas as pd
import geopandas as gpd
import streamlit as st
import folium
from streamlit_folium import st_folium
from shapely.geometry import Point


import matplotlib.pyplot as plt
import seaborn as sns

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


selected_table = st.selectbox(
    "Select a table",
    ["major_city", "city"]
)

selected_df = load_data(selected_table)

cities = selected_df['City'].unique()

selected_cities = st.multiselect("Seleziona le città", cities, default=cities[:5])

df_filtered = selected_df[selected_df['City'].isin(selected_cities)]

    # Analisi temporale
st.subheader("Analisi temporale")
df_filtered['Year'] = pd.to_datetime(df_filtered['dt']).dt.year
avg_temp_per_year = df_filtered.groupby(['Year', 'City'])['AverageTemperature'].mean().reset_index()

    # Visualizzazione
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=avg_temp_per_year, x='Year', y='AverageTemperature', hue='City', ax=ax)
ax.set_title("Variazione delle temperature medie nel tempo")
ax.set_ylabel("Temperatura Media (°C)")
st.pyplot(fig)

    # Statistiche
st.subheader("Statistiche delle variazioni")
temp_variation = df_filtered.groupby('City')['AverageTemperature'].agg(['max', 'min']).reset_index()
temp_variation['Range'] = temp_variation['max'] - temp_variation['min']
st.write(temp_variation)

