import pandas as pd
import pandas as pd
import streamlit as st
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

def multieselector_place(data, colum_name, default_place=['New York', 'Los Angeles']):
    """
    Restituisce la lista delle città selezionate dall'utente nel multiselect.
    Se l'utente non seleziona altre città, restituisce le due città predefinite.

    Parameters:
    - data: DataFrame contenente i dati delle città.
    - default_place: Lista delle due città predefinite (di default 'New York' e 'Los Angeles').

    Returns:
    - place_selected: Lista delle città selezionate dall'utente.
    """
    # Multiselect per selezionare le città, con due città di default
    place_selected = st.multiselect(
        "Seleziona le città",
        options=data[colum_name].unique(),
        default=default_place  # Impostiamo due città di default
    )

    # Se non è stata selezionata nessuna città, usiamo le città predefinite
    if len(place_selected) == 0:
        st.warning("Per favore, seleziona almeno una città.")  # Mostra un avviso se nessuna città è selezionata
        place_selected = default_place  # Se nessuna città è selezionata, rimpiazziamo con le città di default

    return place_selected

# Funzione per creare uno slider che consenta di selezionare un anno
def year_slider(min_year, max_year):
    """
    Crea uno slider per selezionare un intervallo of years.
    
    Parameters:
    - min_year: L'anno minimo.
    - max_year: L'anno massimo.
    
    Returns:
    - selected_year: L'anno selezionato tramite lo slider.
    """
    selected_year_range = st.slider(
        "Seleziona un intervallo di anni",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1
    )
    return selected_year_range

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

