import os
import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

"""No, non è necessario sostituire __file__ con il nome del tuo file. __file__ è una variabile speciale di Python che rappresenta il percorso del file di script attualmente in esecuzione. Questo codice funziona automaticamente per qualsiasi file, ottenendo la directory in cui si trova il file stesso.

Ecco cosa fa il codice:

os.path.abspath(__file__): restituisce il percorso assoluto del file di script in esecuzione.
os.path.dirname(...): ottiene solo la directory di quel percorso.
os.chdir(script_directory): imposta questa directory come directory di lavoro.
Quindi, mantenendo __file__, il codice funziona senza bisogno di modifiche quando lo sposti o lo esegui in directory diverse."""

# Ottieni la directory dello script corrente
script_directory = os.path.dirname(os.path.abspath(__file__))

# Imposta la directory di lavoro sulla posizione dello script
os.chdir(script_directory)


# Titolo dell'app
st.title("Benvenuto nella mia prima app con Streamlit!")

# Creazione di un widget di input di testo
nome = st.text_input("Qual è il tuo nome?")

# Creazione di un pulsante
if st.button("Saluta!"):
    st.write(f"Ciao, {nome}!")

# Grafici e visualizzazione di dati

# Dati casuali
dati = pd.DataFrame(np.random.randn(10, 2), columns=["Colonna 1", "Colonna 2"])
st.line_chart(dati)





# Carica i dati della temperatura per paese
temp_data = pd.read_csv("C:/Users/Francesco/Documenti/GitHub/DSEcoding_project/GlobalLandTemperaturesByCountry.csv")


print(temp_data.head())
"""

# Filtra le righe per evitare valori nulli e seleziona le colonne utili
temp_data = temp_data[['Country', 'AverageTemperature']].dropna()

# Calcola la temperatura media per ogni paese
average_temp_by_country = temp_data.groupby('Country')['AverageTemperature'].mean().reset_index()

# Carica la mappa dei paesi usando geopandas
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Associa i dati delle temperature ai dati geografici
world = world.merge(average_temp_by_country, left_on="name", right_on="Country", how="left")

# Funzione per visualizzare la mappa
def plot_map(data):
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    data.plot(column='AverageTemperature', cmap='coolwarm', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
    plt.title("Temperature Medie per Paese")
    return fig

# Configura l'interfaccia Streamlit
st.title("Mappa delle Temperature Medie Globali")
st.write("Questa mappa mostra le temperature medie dei vari paesi.")

# Mostra la mappa con Streamlit
fig = plot_map(world)
st.pyplot(fig)
"""

"""
import os.path
import zipfile
import pandas as pd
import urllib.request



if not os.path.exists("dataset"):
    print("Downloading dataset...\n")
    urllib.request.urlretrieve("https://drive.usercontent.google.com/download?id=1C_ZIzxojyVbuvkRAGyMdjOqXI0r3ndpT&export=download&authuser=0&confirm=t&uuid=9b7336fe-4c34-4a05-a3cb-9050910b6b37&at=AN_67v2XFPmyMPEvQZFCsujzNMW7%3A1728940914781", "dataset.zip")
    print("Dataset downloaded successfully!\n")

    print("Extracting dataset...\n")
    with zipfile.ZipFile("dataset.zip","r") as zip_ref:
        zip_ref.extractall("dataset")
    print("Dataset extracted successfully!\n")
    os.remove("dataset.zip")

global_temperature_csv               = pd.read_csv('.\\dataset\\GlobalTemperatures.csv').to_dict()
global_temperature_country_df       = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByCountry.csv')
global_temperature_country_csv       = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByCountry.csv').to_dict()
global_temperature_majorcity_csv     = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByMajorCity.csv').to_dict()
global_temperature_city_csv          = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByCity.csv').to_dict()


country = input("Enter the country name: ")

# Filter the data for the specified country
country_data = global_temperature_country_df[global_temperature_country_df['Country'] == country]
"""