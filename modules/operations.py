import numpy as np
import pandas as pd

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
