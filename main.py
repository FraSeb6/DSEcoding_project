import os
import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Ottieni la directory dello script corrente
script_directory = os.path.dirname(os.path.abspath(__file__))

# Imposta la directory di lavoro sulla posizione dello script
os.chdir(script_directory)

APP_TITLE = "Grafic Visualizazation of data on a map"
APP_SUBTITLE = "This is a simple example of how to visualize data on a map using Streamlit and Folium"

def main_graphic_visualization():
    st.set_page_config(page_title=APP_TITLE, page_icon=":earth_americas:", layout="wide")
    st.title(APP_TITLE)
    st.caption(APP_SUBTITLE)
    
    #load data
    
    #display filters and map
    
if __name__ == "__main__":
    main_graphic_visualization()




#No, non è necessario sostituire __file__ con il nome del tuo file. __file__ è una variabile speciale di Python che rappresenta il percorso del file di script attualmente in esecuzione. Questo codice funziona automaticamente per qualsiasi file, ottenendo la directory in cui si trova il file stesso.os.path.abspath(__file__): restituisce il percorso assoluto del file di script in esecuzione.
#os.path.dirname(...): ottiene solo la directory di quel percorso.
#os.chdir(script_directory): imposta questa directory come directory di lavoro.
#Quindi, mantenendo __file__, il codice funziona senza bisogno di modifiche quando lo sposti o lo esegui in directory diverse.






st.title(":red[WHEATHER APP]")
st.subheader(":blue[_The dataset reports the temperature recorded in major cities around the world since 1750.Using this data, the project will need to provide an effective graphical visualization of thechange in temperatures over time, highlighting the cities where the largest temperature ranges were recorded during different historical periods. For visualization of the data on a map, see geopandas.The program will also suggest, depending on the period considered, the best route to follow for a traveler who intends to move from Beijing to Los Angeles by moving step by step to the warmest city among the 3 closest to him._] ")

# Read the GlobalLandTemperaturesByCountry dataset
country                 = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByCountry.csv')
city                    = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByCity.csv')
major_city              = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByMajorCity.csv')
state                   = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByState.csv')
global_temp_country     = pd.read_csv('.\\dataset\\GlobalTemperatures.csv')



st.write(country.head())
st.write(major_city)


start_date = st.date_input('Start date', pd.to_datetime('2000-01-01'))
end_date = st.date_input('End date', pd.to_datetime('2020-01-01'))

# Filter the dataset based on the selected date range
filtered_data = country[(country['dt'] >= str(start_date)) & (country['dt'] <= str(end_date))]

# Display the filtered data
st.write(filtered_data.head())














df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [57.76, 122.4],
    columns=["lat", "lon"],
)
st.map(df)



