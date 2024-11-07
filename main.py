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



import pandas as pd

# Percorsi dei file caricati dall'utente
file_paths = {
    "country_temperatures": "/mnt/data/GlobalLandTemperaturesByCountry.csv",
    "city_temperatures": "/mnt/data/GlobalLandTemperaturesByMajorCity.csv",
    "state_temperatures": "/mnt/data/GlobalLandTemperaturesByState.csv",
    "global_temperatures": "/mnt/data/GlobalTemperatures.csv"
}

# Leggiamo il contenuto dei file
datasets = {name: pd.read_csv(path) for name, path in file_paths.items()}

# Visualizziamo i primi 5 record di ogni dataset per verificarne il contenuto
{key: data.head() for key, data in datasets.items()}


"""


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