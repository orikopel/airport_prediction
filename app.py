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
traffic_path = 'traffic_data.csv'

start_date = datetime(2016, 1, 1)
end_date = datetime(2024, 12, 31)

# ----------------------------------------------- #
# Streamlit App #

# Set up the Streamlit app
st.set_page_config(layout="wide")
st.title("Flight Information Dashboard")

# User input
col1, col2, col3 = st.columns(3)
with col1:
    airport_a = st.text_input("Enter Airport A code")
with col2:
    airport_b = st.text_input("Enter Airport B code")
with col3:
    flight_date = st.date_input("Select Flight Date", value=datetime.now().date())

# data not loaded
if 'data_loaded' not in state:
    state.data_loaded = False

# run predictions and generate visuals
if st.button("Load Flight Information") or state.data_loaded:
    state.data_loaded = True

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

    # create map
    m = make_map(locations_df)

    # store visuals
    state.m = m
    state.plot1 = plot1
    state.plot2 = plot2

# Display the results outside the button click logic
if state.data_loaded:
    col1, col2 = st.columns([3, 2])
    with col1:
        # Display the Folium map
        st.subheader("Flight Route Map")
        st_folium(state.m, width=900, height=900)
    with col2:
        st.subheader("Traffic Prediction")
        st.plotly_chart(state.plot1, use_container_width=True)
        st.plotly_chart(state.plot2, use_container_width=True)
    
    
