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

# Function to find the optimal path between two cities based on a combined score of average temperature and distance to the destination
def find_path(geo_data, start_city, end_city, w_T=0.4, w_D=0.6):
    """
    Finds the optimal path between two cities based on a score that combines
    average temperature and distance to the destination.
    """
    # Find the start and end points
    start = geo_data[geo_data['City'] == start_city]
    end = geo_data[geo_data['City'] == end_city]

    if start.empty or end.empty:
        raise ValueError("One of the specified cities is not in the dataset.")

    # Initialize the path and the current point
    path = [start_city]
    current = start

    while current['City'].values[0] != end_city:
        # Calculate the distance from all cities that have not been visited yet
        remaining = geo_data[~geo_data['City'].isin(path)]

        # Calculate the distance from the current point
        remaining['distance_from_current'] = remaining.geometry.distance(current.geometry.values[0])

        # Select the three closest cities
        closest = remaining.nsmallest(3, 'distance_from_current')

        # Check if the destination city is among the closest cities
        if end_city in closest['City'].values:
            path.append(end_city)
            break

        # Calculate the distance to the destination for the score
        closest['distance_to_dest'] = closest.geometry.distance(end.geometry.values[0])

        # Calculate the combined score
        closest['score'] = (
            w_T * closest['AverageTemperature'] - w_D * closest['distance_to_dest']
        )

        # Choose the city with the highest score
        next_city = closest.loc[closest['score'].idxmax()]

        # Add the selected city to the path
        path.append(next_city['City'])
        current = geo_data[geo_data['City'] == next_city['City']]
    return path
