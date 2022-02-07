from time import time
import numpy as np
import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
import random
from datetime import datetime

# --------------------------------------------------- #
# --------------- DATA READING ---------------------- #
# --------------------------------------------------- #

def get_data(start_date, end_date):
    '''
    This function should return a dataframe with columns such as year, latitude, longitude, comment
    Until raw data is obtained, we'll be using random datapoints
    '''
    data_size = 40
    year_range = list(range(2004, datetime.now().date().year + 1))
    locations_range = [[-41.05056689502945, -71.52142543656218],
                       [-41.0773687745212, -71.52518967193343],
                       [-41.072723962417925, -71.16194679705137]]
    temp_df = pd.DataFrame([{
        'Year':
        random.choice(year_range),
        'Latitude':
        random.random() / 200 + random.choice(locations_range)[0],
        'Longitude':
        random.random() / 100 + random.choice(locations_range)[1]
    } for i in range(data_size)])

    temp_df = temp_df[(temp_df['Year'] <= end_date) & (temp_df['Year'] >= start_date)]
    return temp_df.sort_values(by='Year')


time_range_lower = pd.DataFrame(
    [i for i in range(2004,
                      datetime.now().date().year+1)])

time_range_upper = pd.DataFrame(
    [i for i in range(2004,
                      datetime.now().date().year + 1)])


# --------------------------------------------------- #
# ---------------- STREAMLIT ------------------------ #
# --------------------------------------------------- #
st.set_page_config(
            page_title="Proyectos Virginia", # => Quick reference - Streamlit
            page_icon="🏠",
            layout="centered", # wide
            initial_sidebar_state="auto") # collapsed

st.markdown("""# Proyectos Virginia Bariloche
            """)


### Select dates

st.session_state.lower_time_range = st.selectbox(
    'A partir de que año?',time_range_lower)

time_range_upper = time_range_upper[time_range_upper[0] >= st.session_state.lower_time_range]

st.session_state.upper_time_range = st.selectbox('Hasta que año?',
                                                 time_range_upper)

proyects_df = get_data(st.session_state.lower_time_range,
                       st.session_state.upper_time_range)

# --------------------------------------------------- #
# ---------------- FOLIUM MAP ----------------------- #
# --------------------------------------------------- #

bariloche_coordinates = [-41.13634786671877, -71.31073355248633]
m = folium.Map(location=[bariloche_coordinates[0], bariloche_coordinates[1]],
               zoom_start=11,
               tiles='openstreetmap')

for index,row in proyects_df.iterrows():
    folium.Marker(
        location=[row.Latitude, row.Longitude],
        popup=f'Año Proyecto: {int(row.Year)}',
        # icon=folium.Icon(color=color_guide(row.prediction)),
    ).add_to(m)

folium_static(m)

# --------------------------------------------------- #
# ------------- PROYECT ANALYSIS -------------------- #
# --------------------------------------------------- #

st.markdown(f'''Entre {st.session_state.lower_time_range} y
            {st.session_state.upper_time_range} un
            total de {proyects_df.shape[0]} proyectos fueron realizados.''')
