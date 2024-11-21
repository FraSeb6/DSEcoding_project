import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from modules.operations import *

def display_chart(filtered_data, place_selected, place_column='City', temp_column='AverageTemperature'):
    """
    Function to display the selected chart: Line Chart or Histogram.
    
    Parameters:
    - filtered_data: DataFrame containing the filtered data.
    - place_selected: List of selected cities or countries to display data for.
    - place_column: The column containing the geographic entities (default 'City').
    - temp_column: The column containing the temperature data (default 'AverageTemperature').
    """
    # Radio button to select the type of chart
    chart_type = st.radio(
        "Select the chart type:",
        options=["Line Chart", "Histogram"],
        horizontal=True  # To arrange the options horizontally
    )
    
    # Display the chart based on selection
    if chart_type == "Line Chart":
        # Show the line chart
        plt = plot_temperature_trends(filtered_data, place_selected, place_column, temp_column)
        st.pyplot(plt)

    elif chart_type == "Histogram":
        # Show the histogram of top 7 places with the largest temperature ranges
        fig = plot_temperature_range_histogram(filtered_data, place_column, temp_column)
        st.pyplot(fig)

def plot_temperature_trends(data, places_selected, place_column='City', temp_column='AverageTemperature'):
    """
    Function to plot the line chart of average temperatures over time for the selected entities 
    (cities, countries, states, etc.).
    
    Parameters:
    - data: DataFrame containing the filtered data.
    - places_selected: The list of selected entities (cities, countries, states, etc.).
    - place_column: The name of the column containing the geographic entities (default 'City').
    - temp_column: The name of the column containing the temperatures (default 'AverageTemperature').

    Returns:
    - plt: The plot object to be displayed in Streamlit.
    """
    plt.figure(figsize=(12, 6))
    
    # Iterate over each selected entity
    for place in places_selected:
        place_data = data[data[place_column] == place]
        
        # Group the data by year and calculate the average temperature for each year
        place_data['Year'] = place_data['dt'].dt.year
        annual_temp = place_data.groupby('Year')[temp_column].mean().reset_index()
        
        # Create the line chart for each entity without markers
        plt.plot(annual_temp['Year'], annual_temp[temp_column], 
                 label=place, linewidth=2)  # Without markers

    # Add title, labels, and improve the visual layout
    plt.title(f"Temperature Trends for the Selected {place_column.capitalize()}s", fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Average Temperature (°C)', fontsize=12)
    plt.legend(title=place_column.capitalize(), fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)  # Light grid for better visibility
    plt.xticks(rotation=45)
    plt.tight_layout()  # Improve the arrangement of elements
    return plt



def plot_temperature_range_histogram(data, places_column='City', period_column='dt', temp_column='AverageTemperature'):
    """
    Funzione per mostrare un istogramma delle top 10 entità (città, paesi, stati, ecc.) con i maggiori range di temperatura.
    Se ci sono meno di 10 entità, mostra tutte le entità disponibili.
    
    Parametri:
    - data: DataFrame contenente i dati delle entità con informazioni sulla temperatura.
    - places_column: La colonna che rappresenta l'entità geografica (default 'City').
    - period_column: La colonna che rappresenta il periodo (default 'dt').
    - temp_column: La colonna che contiene i dati delle temperature (default 'AverageTemperature').

    Restituisce:
    - fig: La figura dell'istogramma.
    """
    temperature_ranges = []

    # Converti la colonna del periodo in formato datetime, se non lo è già
    if not pd.api.types.is_datetime64_any_dtype(data[period_column]):
        data[period_column] = pd.to_datetime(data[period_column], errors='coerce')

    # Ottieni le entità uniche (città, paesi, stati, ecc.)
    places_available = data[places_column].unique()

    for place in places_available:
        place_data = data[data[places_column] == place]
        
        # Raggruppa i dati per anno e calcola la temperatura massima e minima per ogni entità
        place_data['Year'] = place_data[period_column].dt.year
        place_range = place_data.groupby('Year')[temp_column].agg(['max', 'min'])
        
        # Calcola il range di temperatura per ogni entità (max - min)
        place_range['TemperatureRange'] = place_range['max'] - place_range['min']
        
        # Aggiungi il range massimo per l'entità
        temperature_ranges.append({
            places_column: place,
            'TemperatureRange': place_range['TemperatureRange'].max()  # Usa il range massimo
        })

    # Crea un DataFrame con i risultati
    temp_range_df = pd.DataFrame(temperature_ranges)

    # Ordina le entità per range di temperatura in ordine decrescente
    temp_range_df_sorted = temp_range_df.sort_values(by='TemperatureRange', ascending=False)

    # Se ci sono meno di 10 entità, seleziona tutte le entità disponibili
    top_n = min(10, len(temp_range_df_sorted))
    temp_range_df_sorted = temp_range_df_sorted.head(top_n)

    # Crea l'istogramma
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(temp_range_df_sorted[places_column], temp_range_df_sorted['TemperatureRange'], color='skyblue')

    # Aggiungi titolo e etichette
    ax.set_title(f'Top {top_n} {places_column.capitalize()}s with the Largest Temperature Range', fontsize=16)
    ax.set_xlabel(places_column.capitalize(), fontsize=12)
    ax.set_ylabel('Temperature Range (°C)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    
    return fig  # Restituisce la figura da visualizzare in Streamlit




##########################################################################################
####  MAP VISUALIZATION  ################################################################

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

def display_map(df):
    map_with_markers = create_map_with_markers(df)
    st_folium(map_with_markers, width=1200, height=800)



##########################################################################################
####  DATA VISUALIZATION ROUTE ###########################################################

# Function to visualize the calculated path on a Folium map
def visualize_path(geo_data, path, start_city, end_city):
    """
    Visualizes the calculated path on a Folium map.
    - The cities in the path are highlighted and connected by a line.
    - Cities not visited are shown with lower opacity and include the temperature in the popup.
    """
    # Create a map centered on the starting city
    start_coords = geo_data[geo_data['City'] == start_city].geometry.values[0]
    m = folium.Map(location=[start_coords.y, start_coords.x], zoom_start=3)

    # Add all cities with low opacity and show temperature in the popup
    for _, row in geo_data.iterrows():
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=4,
            color="gray",
            fill=True,
            fill_color="gray",
            fill_opacity=0.3,
            popup=f"{row['City']}<br>Temp: {row['AverageTemperature']:.2f}°C",
        ).add_to(m)

    # Highlight the cities in the path
    for city in path:
        city_data = geo_data[geo_data['City'] == city]
        city_coords = city_data.geometry.values[0]
        temperature = city_data['AverageTemperature'].values[0]
        folium.CircleMarker(
            location=[city_coords.y, city_coords.x],
            radius=6,
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.6,
            popup=f"{city}<br>Temp: {temperature:.2f}°C",
        ).add_to(m)

    # Connect the cities in the path with a line
    path_coords = [
        [geo_data[geo_data['City'] == city].geometry.y.values[0],
         geo_data[geo_data['City'] == city].geometry.x.values[0]]
        for city in path
    ]
    folium.PolyLine(path_coords, color="blue", weight=2.5, opacity=0.6).add_to(m)

    # Highlight the start city in green and the end city in red
    start_data = geo_data[geo_data['City'] == start_city]
    start_coords = start_data.geometry.values[0]
    start_temp = start_data['AverageTemperature'].values[0]
    folium.CircleMarker(
        location=[start_coords.y, start_coords.x],
        radius=8,
        color="green",
        fill=True,
        fill_color="green",
        fill_opacity=1,
        popup=f"Start: {start_city}<br>Temp: {start_temp:.2f}°C",
    ).add_to(m)

    end_data = geo_data[geo_data['City'] == end_city]
    end_coords = end_data.geometry.values[0]
    end_temp = end_data['AverageTemperature'].values[0]
    folium.CircleMarker(
        location=[end_coords.y, end_coords.x],
        radius=8,
        color="red",
        fill=True,
        fill_color="red",
        fill_opacity=1,
        popup=f"End: {end_city}<br>Temp: {end_temp:.2f}°C",
    ).add_to(m)

    return m