import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import streamlit as st

# Supponiamo di avere un DataFrame con i dati di temperatura
data = {
    "City": ["City1", "City2", "City3", "City4"],
    "Temperature": [-10, 0, 15, 30]
}
df = pd.DataFrame(data)

# Definire la colormap e normalizzare i valori di temperatura
colormap = plt.get_cmap("coolwarm")
norm = plt.Normalize(df["Temperature"].min(), df["Temperature"].max())

# Creare una colonna di colori basata sui valori di temperatura
df["Color"] = df["Temperature"].apply(lambda temp: colormap(norm(temp)))

# Mostrare il DataFrame con i colori su Streamlit
st.dataframe(df)

# Visualizzare un grafico colorato in base alla temperatura
fig, ax = plt.subplots()
sc = ax.scatter(df["City"], df["Temperature"], c=df["Temperature"], cmap="coolwarm", edgecolor="k")
plt.colorbar(sc, ax=ax, label="Temperature (°C)")
plt.xlabel("City")
plt.ylabel("Temperature")
st.pyplot(fig)
