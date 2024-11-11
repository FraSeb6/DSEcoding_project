import streamlit as st
import pandas as pd

# Load the datasets
def load_data():
    country                 = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByCountry.csv')
    city                    = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByCity.csv')
    major_city              = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByMajorCity.csv')
    state                   = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByState.csv')
    global_temp_country     = pd.read_csv('.\\dataset\\GlobalTemperatures.csv')
    return country, city, major_city, state, global_temp_country



#df: This is the DataFrame that contains your data.
#date_column: The name of the column in the DataFrame that contains date values.
#country_column: (countryal) The name of the column that contains country information.
#country_value: (countryal) The specific country value you want to filter by.

def get_min_year(df, date_column, country_column=None, country_value=None):
    df[date_column] = pd.to_datetime(df[date_column])
    if country_column and country_value:
        df = df[df[country_column] == country_value]
    return df[date_column].dt.year.min()

def get_max_year(df, date_column, country_column=None, country_value=None):
    df[date_column] = pd.to_datetime(df[date_column])
    if country_column and country_value:
        df = df[df[country_column] == country_value]
    return df[date_column].dt.year.max()

def get_oldest_month_country(df, date_column, country_column=None, country_value=None):
    df[date_column] = pd.to_datetime(df[date_column])
    if country_column and country_value:
        df = df[df[country_column] == country_value]
    oldest_year = df[date_column].dt.year.min()
    oldest_month = df[df[date_column].dt.year == oldest_year][date_column].dt.month.min()#Questa riga filtra il DataFrame per includere solo le righe dove l'anno della data è uguale all'anno più antico trovato nel passaggio precedente. Poi, estrae il mese da queste date e trova il mese più antico utilizzando il metodo min().
    return oldest_month

def get_last_month_country(df, date_column, country_column=None, country_value=None):
    df[date_column] = pd.to_datetime(df[date_column])
    if country_column and country_value:
        df = df[df[country_column] == country_value]
    last_year = df[date_column].dt.year.max()
    last_month = df[df[date_column].dt.year == last_year][date_column].dt.month.max()
    return last_month

def filter_and_display_data():
    if 'Country' in table_input.columns:
        country_selected = st.selectbox(
            "Select a country",
            table_input['Country'].unique()
        )
        min_year = get_min_year(table_input, 'dt', 'Country', country_selected)
        max_year = get_max_year(table_input, 'dt', 'Country', country_selected)
        oldest_month_country = get_oldest_month_country(country, 'dt', 'Country', country_selected)
        last_month_country = get_last_month_country(country, 'dt', 'Country', country_selected)
    else:
        min_year = get_min_year(table_input, 'dt')
        max_year = get_max_year(table_input, 'dt')
        oldest_month_country = get_oldest_month_country(country, 'dt')
        last_month_country = get_last_month_country(country, 'dt')
    return min_year, max_year, oldest_month_country, last_month_country, country_selected
        
#slider per anni e mesi in base a country
def create_sliders(min_year, max_year, oldest_month_country, last_month_country):
    if 'Country' in table_input.columns:
        year_range = st.slider(        
            "Select a range of years",
            min_value=min_year,         
            max_value=max_year,         
            value=(min_year, max_year)
        )
        if min_year == max_year:
            month_range = st.slider(
                "Select a range of months",
                min_value=oldest_month_country,
                max_value=last_month_country,
                value=(oldest_month_country, last_month_country)
            )
        else:
            if min_year == year_range[0]:
                min_month = oldest_month_country
            else:
                min_month = 1
            if max_year == year_range[1]:
                max_month = last_month_country
            else:
                max_month = 12
            month_range = st.slider(
                "Select a range of months",
                min_value=min_month,
                max_value=max_month,
                value=(min_month, max_month)
            )
    else:
        year_range = st.slider(
            "Select a range of years",
            min_value=min_year,          
            max_value=max_year,          
            value=(min_year, max_year)
        )
        if min_year == max_year:
            month_range = st.slider(
                "Select a range of months",
                min_value=oldest_month_country,
                max_value=last_month_country,
                value=(oldest_month_country, last_month_country)
            )
        else:
            if min_year == year_range[0]:
                min_month = oldest_month_country
            else:
                min_month = 1
            if max_year == year_range[1]:
                max_month = last_month_country
            else:
                max_month = 12
            # Sistemazione dell'indentazione qui:
            month_range = st.slider(
                "Select a range of months",
                min_value=min_month,
                max_value=max_month,
                value=(min_month, max_month)
            )
    return year_range, month_range

# convertitor in dataframe 
def get_dataframe(table):
    if table == "country":
        return country
    elif table == "city":
        return city
    elif table == "major_city":
        return major_city
    elif table == "state":
        return state
    elif table == "global_temp_country":
        return global_temp_country

def get_average_temperature_by_year(df, country, year_range):
    df['dt'] = pd.to_datetime(df['dt'])
    df = df[(df['Country'] == country) & (df['dt'].dt.year >= year_range[0]) & (df['dt'].dt.year <= year_range[1])]
    df['Year'] = df['dt'].dt.year
    return df.groupby('Year')['AverageTemperature'].mean().reset_index()




country, city, major_city, state, global_temp_country = load_data()

table_input = st.selectbox(
    "Select a table",
    ["country", "major_city", "state", "city"]
)

table_input = get_dataframe(table_input)

col1, col2 = st.columns(2)






with col1:
    min_year_input , max_year_input , oldest_month_country_input , last_month_country_input , country_input = filter_and_display_data()

with col2:
    year_range, month_range = create_sliders(min_year_input , max_year_input , oldest_month_country_input , last_month_country_input)

average_temperature_by_year = get_average_temperature_by_year(table_input, country_input, year_range)

if 'Country' in table_input.columns:
    filtered_data = table_input[
        (table_input['Country'] == country_input) &
        (table_input['dt'].dt.year >= year_range[0]) &
        (table_input['dt'].dt.year <= year_range[1]) &
        (table_input['dt'].dt.month >= month_range[0]) &
        (table_input['dt'].dt.month <= month_range[1])
    ]
else:
    filtered_data = table_input[
        (table_input['dt'].dt.year >= year_range[0]) &
        (table_input['dt'].dt.year <= year_range[1]) &
        (table_input['dt'].dt.month >= month_range[0]) &
        (table_input['dt'].dt.month <= month_range[1])
    ]

st.write(filtered_data)

#Visualizza un grafico a linee per la colonna 'AverageTemperature' del DataFrame filtrato.
linechart = st.line_chart(filtered_data.set_index('dt')['AverageTemperature'])
linechart_average = st.line_chart(average_temperature_by_year.set_index('Year')['AverageTemperature'])
