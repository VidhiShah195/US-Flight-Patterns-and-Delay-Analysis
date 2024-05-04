import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import plotly.graph_objects as go

st.set_page_config(
    page_title="Arrival Analysis",
    page_icon='✈️'
    )


# added cache to ensure that the data doesn't have to be reloaded everytime the file runs.
@st.cache_data
def load_data(csv):
    return pd.read_csv(csv)

# reading the csv as a pandas daatframe.
flights_data = load_data("Flight_delay.csv/flights_sample_3m.csv")

# reading the gif file as binary data and then encoding it as a base64, and storing the result as a string.
with open("Flight_delay.csv/landing.gif", "rb") as f:
    gif_data = f.read()
gif_base64 = base64.b64encode(gif_data).decode()

# creating a centrerd layout with the gif and tile being in the same line and there being 10 pixels of space between the gif and title.
st.markdown(
    f"""
    <div style="display: flex; justify-content: center; align-items: center;">
        <img src="data:image/gif;base64,{gif_base64}" alt="gif" width="100">
        <h1 style="margin-left: 10px;"> Arrival Analysis</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# making a gray horizontal line under my title (used just for fun).
st.markdown("<hr style='border: 1px solid #f0f0f0;'>", unsafe_allow_html=True)


# Display select boxes
selected_airport_arr = st.selectbox('Select Arrival Airport', sorted(flights_data['ORIGIN'].unique()))
# Filter airlines based on selected airport
filtered_airlines = flights_data[flights_data['ORIGIN'] == selected_airport_arr]['AIRLINE'].unique()
selected_airline_arr = st.selectbox('Select Airline', sorted(filtered_airlines))



# BUSIEST ARRIVAL TIMES
st.subheader(f'Busiest Arrival Times at {selected_airport_arr} with {selected_airline_arr}')

# converting arrival time to datetime format and then extracting hour from arrival time.
flights_data['CRS_ARR_TIME'] = pd.to_datetime(flights_data['CRS_ARR_TIME'], format='%H%M', errors='coerce')
flights_data['ArrHour'] = flights_data['CRS_ARR_TIME'].dt.hour

# filtering data based on user's selected airport and airline.
filtered_data_arr = flights_data[(flights_data['DEST'] == selected_airport_arr) & (flights_data['AIRLINE'] == selected_airline_arr)]

# counting occurrences of each arrival hour.
arrival_counts = filtered_data_arr['ArrHour'].value_counts().sort_index()

# Define the hours and initialize arrival counts for all hours
hours = [(f'{h % 12 if h % 12 != 0 else 12} {"AM" if h < 12 else "PM"}') for h in range(24)]
arrival_counts_all_hours = {hour: 0 for hour in range(24)}

# Count occurrences of each arrival hour
for hour, count in arrival_counts.items():
    arrival_counts_all_hours[hour] = count

# Make the bar chart
fig1 = px.bar(x=hours, y=[arrival_counts_all_hours[hour] for hour in range(24)],
              labels={'x': 'Arrival Hour', 'y': 'Number of Flights'},
              title=f'Busiest Arrival Times from {selected_airport_arr} with {selected_airline_arr}')

# Formatting x-axis to display in AM/PM format
fig1.update_xaxes(tickmode='array')

# Adding a tooltip
fig1.update_traces(hovertemplate='<b>Arrival Hour:</b> %{x}<br><b>Number of Flights:</b> %{y}<extra></extra>', marker_color='#73C6A2')
st.plotly_chart(fig1)




st.subheader(f'Arrival Delays For {selected_airport_arr} with {selected_airline_arr} Over Time')

# Extracting relevant columns
scatter_data = filtered_data_arr[['FL_DATE', 'ARR_DELAY']]

# Converting FL_DATE to datetime format
scatter_data['FL_DATE'] = pd.to_datetime(scatter_data['FL_DATE'])

# Filtering out negative arrival delays
scatter_data = scatter_data[scatter_data['ARR_DELAY'] >= 0]

# Grouping by FL_DATE and calculating the average arrival delay for each date
scatter_data = scatter_data.groupby('FL_DATE')['ARR_DELAY'].mean().reset_index()

# Making the scatter plot
fig2 = px.scatter(scatter_data, x='FL_DATE', y='ARR_DELAY', title='Average Arrival Delay Over Time',
                  labels={'FL_DATE': 'Date', 'ARR_DELAY': 'Average Arrival Delay (mins)'})
fig2.update_traces(hovertemplate='<b>Date:</b> %{x}<br><b>Average Arrival Delay:</b> %{y} mins<extra></extra>', marker_color='#73C6A2')
fig2.update(layout_coloraxis_showscale=False)
st.plotly_chart(fig2)



# AVERAGE DELAY FOR THE AIRPORT/AIRLINES
st.subheader('Overall Average Arrival Delay')
# Filtering data to include only positive delay values.
scatter_data_positive_delay = scatter_data[scatter_data['ARR_DELAY'] > 0]
# Calculating the average arrival delay for the filtered data
average_arr_delay = scatter_data_positive_delay['ARR_DELAY'].mean()
# Rounding the average delay
rounded_average = round(average_arr_delay)
st.write(f"The average arrival delay for flights landing in {selected_airport_arr} airport with {selected_airline_arr} is approximately {rounded_average} minutes.")



#renaming my columns so that I can use it later to make sure its easy for my users.
filtered_data_arr.rename(columns={'DELAY_DUE_CARRIER': 'Carrier Delay','DELAY_DUE_WEATHER': 'Weather Delay',
                            'DELAY_DUE_NAS': 'NAS Delay','DELAY_DUE_SECURITY': 'Security Delay',
                            'DELAY_DUE_LATE_AIRCRAFT': 'Late Aircraft Delay'}, inplace=True)

st.subheader("Flight Status and Delay Types Distribution for Arrivals")

# calculating flight count for cancelled, delayed, and diverted flights.
flight_status_counts_arrival = {
    "Cancelled": filtered_data_arr['CANCELLED'].sum(),
    "Delayed": filtered_data_arr[filtered_data_arr['ARR_DELAY'] > 0].shape[0],
    "Diverted": filtered_data_arr['DIVERTED'].sum()
}

fig3 = go.Figure()
# making the bigger pie chart with flight overall status.
fig3.add_trace(go.Pie(
    labels=list(flight_status_counts_arrival.keys()),
    values=list(flight_status_counts_arrival.values()),
    textinfo='label+percent', 
    hole=0.5,
    domain={"x": [0, 0.5]},
    legendgroup="Flight Status",
    showlegend=False,
    hovertemplate='<b>Flight Status:</b> %{label}<br>' + '<b>Value:</b> %{value}<br>' + '<b>Percent of Total:</b> %{percent}'))

#  counting delay types.
delay_counts_arrival = filtered_data_arr[['Carrier Delay', 'Weather Delay', 'NAS Delay', 'Security Delay', 'Late Aircraft Delay']].apply(lambda x: (x > 0).sum())

# making a smaller pie chart for the delay types.
fig3.add_trace(go.Pie(
    labels=delay_counts_arrival.index,
    values=delay_counts_arrival.values,
    hole=0.5,
    domain={"x": [0.70, 1]},
    legendgroup="Delay Types",
    hovertemplate='<b>Cause of Delay:</b> %{label}<br>' + '<b>Value:</b> %{value}<br>' + '<b>Percent of Total:</b> %{percent}'))
fig3.update_layout(
    title_text="Flight Status and Delay Types Distribution for Arrivals",
    annotations=[{"text": "Flight Status", "x": 0.19, "y": 0.5, "showarrow": False},{"text": "Delay Types", "x": 0.91, "y": 0.5, "showarrow": False}],
    legend_title=dict(text="<b>Legend</b>"), width=900, height=600)

st.plotly_chart(fig3, use_container_width=True)