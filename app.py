import streamlit as st
from streamlit_folium import st_folium
from streamlit import session_state as state

import pandas as pd
import plotly.express as px
from datetime import datetime

from plot_map import make_map
from predict_traffic import predict_traffic, load_traffic_data

# ----------------------------------------------- #
# Load Data #

airport_details = pd.read_csv("airports.csv")
airport_names = airport_details["name"].astype(str).tolist()
airport_codes = airport_details["icao"].astype(str).tolist()
airport_options = [" - ".join(x) for x in zip(airport_names, airport_codes)]

traffic_path = 'traffic_data.csv'

start_date = datetime(2016, 1, 1)
end_date = datetime(2024, 12, 31)

# ----------------------------------------------- #
# Streamlit App #

# Set up the Streamlit app
st.set_page_config(layout="wide")
st.title("Airport Traffic & Delay Prediction")

# Initialize session state attributes
if 'm' not in state:
    state.m = None
if 'plot1' not in state:
    state.plot1 = None
if 'plot2' not in state:
    state.plot2 = None
if 'data_loaded' not in state:
    state.data_loaded = False

# User input
col1, col2, col3 = st.columns(3)
with col1:
    airport_a_name = st.selectbox("Select Airport A code", airport_options)
    selected_a_code = airport_a_name.split(" - ")[1]

with col2:
    airport_b_name = st.selectbox("Select Airport B code", airport_options)
    selected_b_code = airport_b_name.split(" - ")[1]
    
with col3:
    flight_date = st.date_input("Select Flight Date", value=datetime.now().date())

# run predictions and generate visuals
if st.button("Load Flight Information"):

    # load traffic data for prediction
    airport_data1 = load_traffic_data(traffic_path, airport_a, start_date, end_date)
    airport_data2 = load_traffic_data(traffic_path, airport_b, start_date, end_date)

    # get names data
    name1 = airport_details[airport_details["icao"]==airport_a]["name"].tolist()[0]
    name2 = airport_details[airport_details["icao"]==airport_b]["name"].tolist()[0]

    # perform traffic prediction for each airport
    pred1, plot1 = predict_traffic(airport_data1, flight_date, f"Traffic prediction for {name1}")
    pred2, plot2 = predict_traffic(airport_data2, flight_date, f"Traffic prediction for {name2}")

    # get locations data
    loc1 = airport_details[airport_details["icao"]==airport_a][["longitude", "latitude"]]
    loc1 = [loc1["longitude"].tolist()[0], loc1["latitude"].tolist()[0]]
    loc2 = airport_details[airport_details["icao"]==airport_b][["longitude", "latitude"]]
    loc2 = [loc2["longitude"].tolist()[0], loc2["latitude"].tolist()[0]]

    # create locations df for map
    locations_df = pd.DataFrame({"geo":[loc1, loc2], "name":[name1, name2], "traffic":[pred1, pred2]})
    state.locdf = locations_df

    # store visuals
    state.plot1 = plot1
    state.plot2 = plot2
    state.data_loaded = True

# Display the results outside the button click logic
if state.get('data_loaded', True):
    col1, col2 = st.columns([3, 2])
    with col1:
        # Display the Folium map
        st.subheader("Flight Route Map")
        if state.locdf is not None:
            st.write("Map is available")
            m = make_map(state.locdf)
            st_folium(m, width=900, height=900)
        else:
            st.write("Map is not available")
    with col2:
        st.subheader("Traffic Prediction")
        st.plotly_chart(state.plot1, use_container_width=True)
        st.plotly_chart(state.plot2, use_container_width=True)

    
