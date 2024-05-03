import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import base64
import geopandas as gpd
import folium
from streamlit_folium import folium_static


st.set_page_config(
    page_title="Arrivals",
    layout='wide',
    page_icon='✈️'
    )


# added cache to ensure that the data doesn't have to be reloaded everytime the file runs.
@st.cache_data
def load_data(csv):
    return pd.read_csv(csv)

flights_data = load_data("Flight_delay.csv/flights_sample_3m.csv")

# reading the gif file as binary data and then encoding it as a base64, and storing the result as a string.
with open("Flight_delay.csv/landing.gif", "rb") as f:
    gif_data = f.read()
gif_base64 = base64.b64encode(gif_data).decode()

# creates a centrerd layout with the gif and tile being in the same line with the title being black 
# and there being 10 pixels of space between the gif and title.
st.markdown(
    f"""
    <div style="display: flex; justify-content: center; align-items: center;">
        <img src="data:image/gif;base64,{gif_base64}" alt="gif" width="100">
        <h1 style="margin-left: 10px;">Flight Arrival Analysis</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# making a gray horizontal line under my title (used just for fun).
st.markdown("<hr style='border: 1px solid #f0f0f0;'>", unsafe_allow_html=True)



# DISTRIBUTION OF DELAY BASED ON USER's SELECTION
st.header('Distribution of Arrival Delay by Selected Arrival Airport and Airlines')
selected_airport_arrival = st.selectbox('Select Arrival Airport', flights_data['DEST'].unique())
selected_airline_arrival = st.selectbox('Select Airline', flights_data['AIRLINE'].unique())

# filter data based on user's selection.
filtered_data_arrival = flights_data[(flights_data['DEST'] == selected_airport_arrival) & (flights_data['AIRLINE'] == selected_airline_arrival)]

# filter arrival delays.
arrival_delayed_flights = filtered_data_arrival[filtered_data_arrival['ARR_DELAY'] > 0]

# making a histogram to show arrival delays distribution.
fig_arr_delay = px.histogram(arrival_delayed_flights, x='ARR_DELAY', nbins=20, 
                             title='Arrival Delays Distribution',
                             labels={'ARR_DELAY': 'Arrival Delay (mins)', 'count': 'Count'}
                            )
fig_arr_delay.update_traces(marker_line=dict(color='black', width=1), 
                            hovertemplate='<b>Arrival Delay:</b> %{x} mins<br><b>Count:</b> %{y}<extra></extra>')
fig_arr_delay.update_layout(barmode='overlay', hovermode='closest') 
st.plotly_chart(fig_arr_delay)

# AVERAGE DELAY FOR THE AIRPORT/AIRLINES
st.header('Average Arrival Delay')
average_arr_delay = arrival_delayed_flights['ARR_DELAY'].mean()
st.write(f"The average arrival delay for flights arriving at {selected_airport_arrival} with {selected_airline_arrival} is {average_arr_delay} minutes.")

# BUSIEST ARRIVAL TIMES
st.header(f'Busiest Arrival Times Based on Selected Arrival Airport and Airlines')

# converting arrival time to datetime format.
flights_data['CRS_ARR_TIME'] = pd.to_datetime(flights_data['CRS_ARR_TIME'], format='%H%M', errors='coerce')

# extracting hour from arrival time.
flights_data['ArrHour'] = flights_data['CRS_ARR_TIME'].dt.hour

# filtering data based on user's selected airport and airline.
filtered_data_arrival = flights_data[(flights_data['DEST'] == selected_airport_arrival) & (flights_data['AIRLINE'] == selected_airline_arrival)]

# counting occurrences of each arrival hour.
arrival_counts = filtered_data_arrival['ArrHour'].value_counts().sort_index()

# making the bar chart
fig = px.bar(arrival_counts, x=arrival_counts.index, y=arrival_counts.values,
             labels={'x': 'Arrival Hour', 'y': 'Number of Flights'},
             title=f'Busiest Arrival Times at {selected_airport_arrival} with {selected_airline_arrival}')

# formatting x-axis to display in AM/PM format.
hours = [(f'{h % 12 if h % 12 != 0 else 12} {"AM" if h < 12 else "PM"}') for h in range(24)]
fig.update_xaxes(tickvals=list(range(24)), ticktext=hours)
fig.update_layout(xaxis=dict(tickmode='array'))

# adding a tooltip.
fig.update_traces(hovertemplate='<b>Arrival Hour:</b> %{x}<br><b>Number of Flights:</b> %{y}<extra></extra>')
st.plotly_chart(fig)




# renaming columns for clarity
filtered_data_arrival.rename(columns={'DELAY_DUE_CARRIER': 'Carrier Delay','DELAY_DUE_WEATHER': 'Weather Delay',
                              'DELAY_DUE_NAS': 'NAS Delay','DELAY_DUE_SECURITY': 'Security Delay',
                              'DELAY_DUE_LATE_AIRCRAFT': 'Late Aircraft Delay'}, inplace=True)

st.header("Flight Status and Delay Types Distribution for Arrivals")

# calculating flight count for cancelled, delayed, and diverted flights.
flight_status_counts_arrival = {
    "Cancelled": filtered_data_arrival['CANCELLED'].sum(),
    "Delayed": filtered_data_arrival[filtered_data_arrival['ARR_DELAY'] > 0].shape[0],
    "Diverted": filtered_data_arrival['DIVERTED'].sum()
}

# counting delay types.
delay_counts_arrival = filtered_data_arrival[['Carrier Delay', 'Weather Delay', 'NAS Delay', 'Security Delay', 'Late Aircraft Delay']].sum()

# making the bigger pie chart with flight overall status.
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=list(flight_status_counts_arrival.keys()),
    values=list(flight_status_counts_arrival.values()),
    textinfo='label+percent', 
    hole=0.5,
    domain={"x": [0, 0.5]},
    legendgroup="Flight Status",
    showlegend=False,
    hovertemplate='<b>Flight Status:</b> %{label}<br>' + '<b>Value:</b> %{value}<br>' + '<b>Percent of Total:</b> %{percent}'))

# making a smaller pie chart for the delay types.
fig.add_trace(go.Pie(
    labels=delay_counts_arrival.index,
    values=delay_counts_arrival.values,
    hole=0.5,
    domain={"x": [0.70, 1]},
    legendgroup="Delay Types",
    hovertemplate='<b>Cause of Delay:</b> %{label}<br>' + '<b>Value:</b> %{value}<br>' + '<b>Percent of Total:</b> %{percent}'))

fig.update_layout(
    title_text="Flight Status and Delay Types Distribution for Arrivals",
    annotations=[{"text": "Flight Status", "x": 0.19, "y": 0.5, "showarrow": False},{"text": "Delay Types", "x": 0.91, "y": 0.5, "showarrow": False}],
    legend_title=dict(text="<b>Legend</b>") 
)
st.plotly_chart(fig, use_container_width=True)








