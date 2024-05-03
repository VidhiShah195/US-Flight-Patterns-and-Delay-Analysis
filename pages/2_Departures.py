import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import plotly.graph_objects as go


st.set_page_config(
    page_title="Departures",
    layout='wide',
    page_icon='✈️'
    )


# added cache to ensure that the data doesn't have to be reloaded everytime the file runs.
@st.cache_data
def load_data(csv):
    return pd.read_csv(csv)

flights_data = load_data("Flight_delay.csv/flights_sample_3m.csv")

with open("Flight_delay.csv/take-off.gif", "rb") as f:
    gif_data = f.read()
gif_base64 = base64.b64encode(gif_data).decode()

# creates a centrerd layout with the gif and tile being in the same line and there being 10 pixels of space between the gif and title.
st.markdown(
    f"""
    <div style="display: flex; justify-content: center; align-items: center;">
        <img src="data:image/gif;base64,{gif_base64}" alt="gif" width="100">
        <h1 style="margin-left: 10px;"> Departure Analysis</h1>
    </div>
    """,
    unsafe_allow_html=True
)
# making a gray horizontal line under my title for a visual division.
st.markdown("<hr style='border: 1px solid #f0f0f0;'>", unsafe_allow_html=True)

selected_airport_dep = st.selectbox('Select Departure Airport', flights_data['ORIGIN'].unique())
selected_airline_dep = st.selectbox('Select Airline', flights_data['AIRLINE'].unique())




# BUSIEST DEPARTURE TIMES
st.subheader(f'Busiest Departure Times at {selected_airport_dep} with {selected_airline_dep}')

# converting departure time to datetime forma and then extracting hour from departure time.
flights_data['CRS_DEP_TIME'] = pd.to_datetime(flights_data['CRS_DEP_TIME'], format='%H%M', errors='coerce')
flights_data['DepHour'] = flights_data['CRS_DEP_TIME'].dt.hour

# filtering data based on user's selected airport and airline.
filtered_data_dep = flights_data[(flights_data['ORIGIN'] == selected_airport_dep) & (flights_data['AIRLINE'] == selected_airline_dep)]

# counting occurrences of each departure hour.
departure_counts = filtered_data_dep['DepHour'].value_counts().sort_index()

# making the bar chart
fig1 = px.bar(departure_counts, x=departure_counts.index, y=departure_counts.values,
             labels={'x': 'Departure Hour', 'y': 'Number of Flights'},
             title=f'Busiest Departure Times from {selected_airport_dep} with {selected_airline_dep}')

# formatting x-axis to display in AM/PM format.
hours = [(f'{h % 12 if h % 12 != 0 else 12} {"AM" if h < 12 else "PM"}') for h in range(24)]
fig1.update_xaxes(tickvals=list(range(24)), ticktext=hours)
fig1.update_layout(xaxis=dict(tickmode='array'))

# adding a tooltip
fig1.update_traces(hovertemplate='<b>Departure Hour:</b> %{x}<br><b>Number of Flights:</b> %{y}<extra></extra>', marker_color='#048092')
st.plotly_chart(fig1)



st.subheader(f'Departure Delays For {selected_airport_dep} with {selected_airline_dep} Over Time')

# extracting relevant columns and sorting the data by flight date.
scatter_data = filtered_data_dep[['FL_DATE', 'DEP_DELAY']]
scatter_data.sort_values(by='FL_DATE', inplace=True)

# filtering data to include only positive delay values.
scatter_data_positive_delay = scatter_data[scatter_data['DEP_DELAY'] > 0]

# making the scatter plot
fig2 = px.scatter(scatter_data_positive_delay, x='FL_DATE', y='DEP_DELAY', title='Departure Delay Over Time',
                labels={'FL_DATE': 'Date', 'DEP_DELAY': 'Departure Delay (mins)'})
fig2.update_traces(hovertemplate='<b>Date:</b> %{x}<br><b>Departure Delay:</b> %{y} mins<extra></extra>', marker_color='#048092')
fig2.update(layout_coloraxis_showscale=False)
st.plotly_chart(fig2)



# AVERAGE DELAY FOR THE AIRPORT/AIRLINES
st.subheader('Average Departure Delay')
average_dep_delay = scatter_data_positive_delay['DEP_DELAY'].mean()
rounded_average = round(average_dep_delay)
st.write(f"The average departure delay for flights departing from {selected_airport_dep} with {selected_airline_dep} is approximately {rounded_average} minutes.")



st.subheader("Flight Status and Delay Types Distribution for Departures")

# renaming my columns so that I can use it later to make sure its easy for my users 
filtered_data_dep.rename(columns={'DELAY_DUE_CARRIER': 'Carrier Delay','DELAY_DUE_WEATHER': 'Weather Delay',
                              'DELAY_DUE_NAS': 'NAS Delay','DELAY_DUE_SECURITY': 'Security Delay',
                              'DELAY_DUE_LATE_AIRCRAFT': 'Late Aircraft Delay'}, inplace=True)


# calculating flight count for cancelled, delayed and or diverted flights.
flight_status_counts = {
    "Cancelled": filtered_data_dep['CANCELLED'].sum(),
    "Delayed": filtered_data_dep[filtered_data_dep['DEP_DELAY'] > 0].shape[0],
    "Diverted": filtered_data_dep['DIVERTED'].sum()
}

# counting delay types.
delay_counts = filtered_data_dep[['Carrier Delay', 'Weather Delay', 'NAS Delay', 'Security Delay', 'Late Aircraft Delay']].sum()

# making the bigger pie chart with flight overall status.
fig3 = go.Figure()

fig3.add_trace(go.Pie(
    labels=list(flight_status_counts.keys()),
    values=list(flight_status_counts.values()),
    textinfo='label+percent', 
    hole=0.5,
    domain={"x": [0, 0.5]},
    legendgroup="Flight Status",
    showlegend=False,
    hovertemplate='<b>Flight Status:</b> %{label}<br>' + '<b>Value:</b> %{value}<br>' + '<b>Percent of Total:</b> %{percent}'))

# making a smaller pie chart for the delay types.
fig3.add_trace(go.Pie(
    labels=delay_counts.index,
    values=delay_counts.values,
    hole=0.5,
    domain={"x": [0.70, 1]},
    legendgroup="Delay Types",
    hovertemplate='<b>Cause of Delay:</b> %{label}<br>' + '<b>Value:</b> %{value}<br>' + '<b>Percent of Total:</b> %{percent}'))

fig3.update_layout(
    title_text="Flight Status and Delay Types Distribution",
    annotations=[{"text": "Flight Status", "x": 0.19, "y": 0.5, "showarrow": False},{"text": "Delay Types", "x": 0.91, "y": 0.5, "showarrow": False}],
    legend_title=dict(text="<b>Legend</b>") 
)
st.plotly_chart(fig3, use_container_width=True)
