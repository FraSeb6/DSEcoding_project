import streamlit as st
import pandas as pd
from modules.data_processing import *
from modules.visualization import *
from modules.operations import *

# Set the page title
st.set_page_config(page_title="Dataset Table", layout="wide")
st.title("TABLE OF GLOBAL TEMPERATURE DATA")

# Carica il dataset delle città
dataset_option = st.sidebar.radio(
    "Seleziona un dataset da visualizzare",
    options=["major_city", "state", "country", "city"]
)

# Carica il dataset
data = load_data(dataset_option)

if dataset_option == "major_city" or dataset_option == "city":
    st.write(f"Dataset: {dataset_option}")
    
    # Converte la colonna 'dt' in formato datetime
    data = convert_to_datetype(data, 'dt')

    # Ottieni l'intervallo degli anni
    min_year, max_year = get_year_range(data, 'dt')

    # Ottieni la lista delle città selezionate, con le due città di default
    cities_selected = multieselector_place(data, 'City', default_place=['New York', 'Los Angeles'])

    # Filtro dei dati in base alle città selezionate
    filtered_data_for_desc = filter_data_by_year(data, 'dt', min_year, max_year)
    filtered_data_for_desc = filtered_data_for_desc[filtered_data_for_desc['City'].isin(cities_selected)]

    # Calcola le statistiche descrittive per le città selezionate
    stats_df = generate_stats_df(filtered_data_for_desc, cities_selected, 'City', 'AverageTemperature')

    # Mostra la tabella delle statistiche descrittive con i nomi delle città come indice
    st.write("Statistiche Descrittive delle Temperature per le Città Selezionate:")
    st.dataframe(stats_df)

    # Range slider per selezionare un intervallo di anni
    selected_year_range = year_slider(min_year, max_year)

    # Filtra i dati in base all'intervallo di anni selezionato
    filtered_data = filter_data_by_year(data, 'dt', selected_year_range[0], selected_year_range[1])

    # Mostra il grafico in base alla selezione
    # Per tracciare il grafico selezionato per le città
    display_chart(filtered_data, place_selected=cities_selected, place_column='City', temp_column='AverageTemperature')



elif dataset_option == "state" or dataset_option == "country":
    st.write(f"Dataset: {dataset_option}")
    
    # Converte la colonna 'dt' in formato datetime
    data = convert_to_datetype(data, 'dt')

    # Ottieni l'intervallo degli anni
    min_year, max_year = get_year_range(data, 'dt')

    # Ottieni la lista delle città selezionate, con le due città di default
    countries_selected = multieselector_place(data, 'Country', default_place=['United States', 'Canada'])

    # Filtro dei dati in base alle città selezionate
    filtered_data = filter_data_by_year(data, 'dt', min_year, max_year)
    filtered_data = filtered_data[filtered_data['Country'].isin(countries_selected)]

    # Calcola le statistiche descrittive per le città selezionate
    stats_df = generate_stats_df(filtered_data, countries_selected, 'Country')

    # Mostra la tabella delle statistiche descrittive con i nomi delle città come indice
    st.write("Statistiche Descrittive delle Temperature per le Città Selezionate:")
    st.dataframe(stats_df)

    # Range slider per selezionare un intervallo di anni
    selected_year_range = year_slider(min_year, max_year)

    # Filtra i dati in base all'intervallo di anni selezionato
    filtered_data = filter_data_by_year(data, 'dt', selected_year_range[0], selected_year_range[1])

    # Mostra il grafico in base alla selezione
    # Per tracciare il grafico selezionato per le città
    # Per tracciare il grafico selezionato per i paesi
    display_chart(filtered_data, place_selected=countries_selected, place_column='Country', temp_column='AverageTemperature')



else:
    st.write("Dataset non valido o assente.")
