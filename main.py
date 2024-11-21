import streamlit as st

# Titolo principale
st.title("Analisi delle Temperature Globali 🌍")

# Introduzione
st.write(
    """
    Benvenuto! Questo progetto ti permette di esplorare i dati sulle temperature globali.
    Utilizza il menu a sinistra per selezionare un dataset e visualizzare le tendenze nel tempo.
    """
)

# Navigazione tra le pagine
page = st.sidebar.selectbox("Seleziona una pagina:", ["Introduzione", "Analisi Dataset"])

# Gestione delle pagine
if page == "Introduzione":
    st.write(
        """
        ### Introduzione
        Questo progetto fornisce strumenti per analizzare l'andamento delle temperature globali
        attraverso diversi dataset. Scegli una pagina dal menu a sinistra per iniziare.
        """
    )
elif page == "Analisi Dataset":
      # Richiama la pagina di analisi
