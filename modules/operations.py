import numpy as np
import pandas as pd
import streamlit as st

def descriptive_stats(data, temp_column):
    """
    Calcola le statistiche descrittive per una colonna di temperature in un DataFrame.
    Aggiunge anche il range di temperatura (max - min).

    Parameters:
    - data: DataFrame contenente i dati.
    - temp_column: Il nome della colonna contenente le temperature.

    Returns:
    - stats: Dizionario contenente le statistiche descrittive (min, max, mean, median, std, range).
    """
    # Rimuovi NaN
    temperatures = data[temp_column].dropna()
    
    # Calcola le statistiche descrittive
    stats = {
        "Minima": np.min(temperatures),
        "Massima": np.max(temperatures),
        "Range": np.max(temperatures) - np.min(temperatures),
        "Media": np.mean(temperatures),
        "Q1": np.percentile(temperatures, 25),
        "Mediana": np.median(temperatures),
        "Q3": np.percentile(temperatures, 75),
        "Deviazione Standard": np.std(temperatures),
        "IQR": np.percentile(temperatures, 75) - np.percentile(temperatures, 25),
        "Numero di Osservazioni": len(temperatures),
        "Varianza": np.var(temperatures),
        "Coefficiente di Variazione": np.std(temperatures) / np.mean(temperatures),
        
    }
    
    return stats



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

def filter_data_by_oneyear(df, date_column, year):
    df_filtered = df[df[date_column].dt.year == year]
    return df_filtered

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

def year_monoslider(min_year=1751, max_year=2011):
    selected_year = st.slider(
        "Select a year",
        min_value=min_year,
        max_value=max_year,
        value=2002
    )
    return selected_year

def month_slider(min_month, max_month):
    selected_month = st.slider(
        "Select a month",
        min_value=min_month,
        max_value=max_month,
        value=9
    )
    return selected_month