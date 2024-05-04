import streamlit as st
import pandas as pd
import plotly.express as px
import base64

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

# reading the gif file as binary data and then encoding it as a base64, and storing the result as a string.
with open("Flight_delay.csv/airport.gif", "rb") as f:
    gif_data = f.read()
gif_base64 = base64.b64encode(gif_data).decode()


# creating a centrerd layout with the gif and tile being in the same line and there being 10 pixels of space between the gif and title.
st.markdown(
    f"""
    <div style="display: flex; justify-content: center; align-items: center;">
        <img src="data:image/gif;base64,{gif_base64}" alt="gif" width="100">
        <h1 style="margin-left: 10px;">Overall Flight Patterns and Delay Analysis in the US</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# making a gray horizontal line under my title (used just for fun).
st.markdown("<hr style='border: 1px solid #f0f0f0;'>", unsafe_allow_html=True)
st.write("The goal of this Streamlit app is to help you navigate and understand the overall flight patterns, including those related to cancellations and delays from January to August of 2023.")

# converting 'FL_DATE' column to datetime.
flights_data['FL_DATE'] = pd.to_datetime(flights_data['FL_DATE'])








st.subheader('Busiest Times at Selected Airport with Selected Airlines (Departure vs Arrival)')
# Display select boxes
dep_arr = st.selectbox('Select Direction', ['Departure', 'Arrival'])
if dep_arr == 'Departure':
    selected_airport = st.selectbox('Select Departure Airport', sorted(flights_data['ORIGIN'].unique()))
    filtered_airlines = flights_data[flights_data['ORIGIN'] == selected_airport]['AIRLINE'].unique()
    selected_airline = st.selectbox('Select Airline', sorted(filtered_airlines))
    filtered_data = flights_data[(flights_data['ORIGIN'] == selected_airport) & (flights_data['AIRLINE'] == selected_airline)]
    title = f'Busiest Departure Times from {selected_airport} with {selected_airline}'
    hour_column = 'CRS_DEP_TIME'
elif dep_arr == 'Arrival':
    selected_airport = st.selectbox('Select Arrival Airport', sorted(flights_data['DEST'].unique()))
    filtered_airlines = flights_data[flights_data['DEST'] == selected_airport]['AIRLINE'].unique()
    selected_airline = st.selectbox('Select Airline', sorted(filtered_airlines))
    filtered_data = flights_data[(flights_data['DEST'] == selected_airport) & (flights_data['AIRLINE'] == selected_airline)]
    title = f'Busiest Arrival Times at {selected_airport} with {selected_airline}'
    hour_column = 'CRS_ARR_TIME'

# Convert time to datetime and extract hour
filtered_data[hour_column] = pd.to_datetime(filtered_data[hour_column], format='%H%M', errors='coerce')
filtered_data['Hour'] = filtered_data[hour_column].dt.hour

# Count occurrences of each hour
hourly_counts = filtered_data['Hour'].value_counts().sort_index()

# Define hours and initialize counts
hours = [(f'{h % 12 if h % 12 != 0 else 12} {"AM" if h < 12 else "PM"}') for h in range(24)]
hourly_counts_all = {hour: 0 for hour in range(24)}

# Count occurrences of each hour
for hour, count in hourly_counts.items():
    hourly_counts_all[hour] = count

# Make the bar chart
fig = px.bar(x=hours, y=[hourly_counts_all[hour] for hour in range(24)],
             labels={'x': 'Hour', 'y': 'Number of Flights'},
             title=title)

# Formatting x-axis to display in AM/PM format
fig.update_xaxes(tickmode='array')

# Adding a tooltip
fig.update_traces(hovertemplate='<b>Hour:</b> %{x}<br><b>Number of Flights:</b> %{y}<extra></extra>', marker_color='#048092')

st.plotly_chart(fig)







# DONUT CHART
st.subheader("Overall Distribution of Flight Status")
st.write("The donut chart below shows the distibution in percentage of the flights that were delayed, cancelled or diverted.")

# counting delayed, diverted, and cancelled flights and then creating a dataframe with it.
delayed_count = len(flights_data[flights_data['ARR_DELAY'] > 0])
diverted_count = len(flights_data[flights_data['DIVERTED'] == 1])
cancelled_count = len(flights_data[flights_data['CANCELLED'] == 1])
flight_status_counts = pd.DataFrame({
    'Status': ['Delayed', 'Diverted', 'Cancelled'],
    'Count': [delayed_count, diverted_count, cancelled_count]
})

# making the chart.
fig5 = px.pie(flight_status_counts, values='Count', names='Status', hole=0.5, title='Distribution of Flight Status')
fig5.update_traces(textinfo='percent+label', hovertemplate='<b>Flight Status:</b> %{label}<br><b>Total Flights:</b> %{value}')
st.plotly_chart(fig5)





# BAR CHART FOR TOP 5 AIRPORTS DUE TO SELECTED DELAY TYPES
st.subheader('Top 5 Airports by Delay Type')
st.write("The bar chart below shows the top 5 busiest airports based on the chosen delay type.")
st.markdown("<b>There are five types of delays:</b> ", unsafe_allow_html=True)
st.markdown("<b> 1. Carrier Delay ✈</b> Delay caused due to carrier, for example maintenance, crew problems, aircraft cleaning, fueling, etc.", unsafe_allow_html=True)
st.markdown("<b> 2. Weather Delay ✈</b> Delay due to extreme weather conditions.", unsafe_allow_html=True)
st.markdown("<b> 3. NAS Delay ✈</b> Delay by National Aviation System (NAS) caused due to non-extreme weather conditions, airport operations, heavy traffic volumes, air traffic control, etc.", unsafe_allow_html=True)
st.markdown("<b> 4. Security Delay ✈</b> Delay caused by security related issues, such as terminal evacuations, aircraft re-boarding due to security breaches, malfunctioning screening equipment, or long queues exceeding 29 minutes at screening areas.", unsafe_allow_html=True)
st.markdown("<b> 5. Late Aircraft Delay ✈</b> Delay due to delayed aircrafts.", unsafe_allow_html=True)

flights_data.rename(columns={'DELAY_DUE_CARRIER': 'Carrier Delay', 'DELAY_DUE_WEATHER': 'Weather Delay',
                             'DELAY_DUE_NAS': 'NAS Delay', 'DELAY_DUE_SECURITY': 'Security Delay', 
                             'DELAY_DUE_LATE_AIRCRAFT': 'Late Aircraft Delay'}, inplace=True)

# filtering delayed flights.
delayed_flights = flights_data[flights_data['ARR_DELAY'] > 0]

# create a list of reasons for delay and then adding a selectbox to choose from the list.
delay_reasons = ['Carrier Delay', 'Weather Delay', 'NAS Delay', 'Security Delay', 'Late Aircraft Delay']
selected_reason = st.selectbox("Select Reason for Delay:", delay_reasons)

# filtering data based on selected delay reason.
if selected_reason != 'DELAY_DUE_LATE_AIRCRAFT':  
    delayed_flights = delayed_flights[delayed_flights[selected_reason] > 0]

# count delayed flights by airport.
delayed_by_airport = delayed_flights.groupby('DEST')['FL_NUMBER'].count().reset_index()
delayed_by_airport.columns = ['Airport', 'DelayedFlights']

# sort and slecting top 5 airports by the number of delayed flights.
delayed_by_airport_sorted = delayed_by_airport.sort_values(by='DelayedFlights', ascending=False)
top_5_airports = delayed_by_airport_sorted.head(5)
top_5_airports_sorted = top_5_airports.sort_values(by='DelayedFlights', ascending=True)

# making the horizontal bar chart for the top 5 airports.
fig6 = px.bar(top_5_airports_sorted, y='Airport', x='DelayedFlights',
             title=f'Top 5 Airports with the Highest Number of Delayed Flights due to {selected_reason}',
             labels={'Airport': 'Airport Code', 'DelayedFlights': 'Number of Delayed Flights'},
             orientation='h')
fig6.update_traces(hovertemplate='<b>Airport:</b> %{y}<br><b>Number of Delayed Flights:</b> %{x:,.0f}<extra></extra>', marker_color='#048092')
st.plotly_chart(fig6)