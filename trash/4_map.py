import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
import folium
from streamlit_folium import folium_static



st.set_page_config(
    page_title="Home: Flight Delay and Cancelation Data Analysis",
    page_icon='✈️'
    )

# added cache to ensure that the data doesn't have to be reloaded everytime the file runs.
@st.cache_data
def load_data(csv):
    return pd.read_csv(csv)

# reading the csv as a pandas daatframe.
flights_data = load_data("Flight_delay.csv/flights_sample_3m.csv")



# MAP SHOULD WORK PERFECTLY FINE WIHT NOTHING BEING SHOWN ON THE MAP AND IT NEVER LOADING
st.header('Map of Flights Landing in Chosen Airport based on the Airlines')
st.write("The map below displays the flights landing in your chosen airport destination based on the airlines.")
# added cache for my shape file to ensure that the data doesn't have to be reloaded everytime the file runs.
@st.cache_data
def load_shp_file(shp):
    return gpd.read_file(shp)

# using the above defined function to read my shape file.
gdf = load_shp_file("geo_data/USA_Airports.shp")

# st.write(gdf)

# mergeing datasets based on ORIGIN and FAA_ID.
merged_data = pd.merge(flights_data, gdf, left_on='ORIGIN', right_on='FAA_ID', how='inner')

# creating two select boxes for my uses to pick the destination airport and airline.
dest_airport = st.selectbox("Select Destination Airport:", merged_data['DEST'].unique())
airline = st.selectbox("Select Airline:", merged_data['AIRLINE'].unique())

# filtering data based on user's selections.
filtered_data = merged_data[(merged_data['DEST'] == dest_airport) & (merged_data['AIRLINE'] == airline)]

# getting latitude and longitude for the destination airport.
selected_dest_row = merged_data[merged_data['DEST'] == dest_airport].iloc[-1]
dest_lat = selected_dest_row['geometry'].y
dest_lon = selected_dest_row['geometry'].x

# creating a folium map centered at the destination airport.
m = folium.Map(location=[dest_lat, dest_lon], zoom_start=4)

# iterating over each row in the filtered_data DataFrame and adding a marker with airoplane on it at the airports with tooltips
for idx, row in filtered_data.iterrows():
    origin_lat = row['geometry'].y
    origin_lon = row['geometry'].x
    origin_airport = row['ORIGIN']
    folium.Marker(location=[origin_lat, origin_lon],
                  icon=folium.Icon(icon='plane', prefix='fa'),
                  popup=f"<b>Route: </b> <br>{row['ORIGIN_CITY']}   ✈   {row['DEST_CITY']}<br>"
                          f"<br><b>Carrier: </b> {row['AIRLINE']}<br>"
                          f"<br> <b>Number of Flights:</b> {row['FL_NUMBER']}<br>"
                          f"<br><b>Avg. Arrival Delay: </b>{row['ARR_DELAY']}<br>").add_to(m)

folium_static(m)