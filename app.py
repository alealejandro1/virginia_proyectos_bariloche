from time import time
import numpy as np
import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
import random
from datetime import datetime
import matplotlib.pyplot as plt

# --------------------------------------------------- #
# --------------- DATA READING ---------------------- #
# --------------------------------------------------- #

def get_data(start_date, end_date):
    '''
    This function should return a dataframe with columns such as year, latitude, longitude, comment
    Until raw data is obtained, we'll be using random datapoints
    '''
    data_size = 10
    year_range =[2004,2005,2006,2007,2008,2009]
    temp_df = pd.DataFrame([{'Year':random.choice(year_range),'Latitude':random.random()/50-41.071,
    'Longitude':random.random()/10-71.17} for i in range(data_size)])

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
               tiles='stamenwatercolor')

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

# st.bar_chart(np.histogram(proyects_df.Year)[0],
#              columns=np.histogram(proyects_df.Year)[1])

fig, ax = plt.subplots()
plt.figure(figsize=(16,6))
fig = proyects_df.Year.hist()
st.pyplot(fig)
