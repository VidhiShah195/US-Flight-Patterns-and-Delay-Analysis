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

# creates a centrerd layout with the gif and tile being in the same line with the title being black 
# and there being 10 pixels of space between the gif and title.
st.markdown(
    f"""
    <div style="display: flex; justify-content: center; align-items: center;">
        <img src="data:image/gif;base64,{gif_base64}" alt="gif" width="100">
        <h1 style="margin-left: 10px;"> Flight Departure Analysis</h1>
    </div>
    """,
    unsafe_allow_html=True
)
# making a gray horizontal line under my title (used just for fun).
st.markdown("<hr style='border: 1px solid #f0f0f0;'>", unsafe_allow_html=True)



# DISTIBUTITON OF DELAY BASED ON USER's SELECTION
st.header('Distribution of Departure Delay by Selected Departure Airport and Airlines')
selected_airport = st.selectbox('Select Departure Airport', flights_data['ORIGIN'].unique())
selected_airline = st.selectbox('Select Airline', flights_data['AIRLINE'].unique())

#  filter data based on user's selection.
filtered_data = flights_data[(flights_data['ORIGIN'] == selected_airport) & (flights_data['AIRLINE'] == selected_airline)]

# filter departure delays.
departure_delayed_flights = filtered_data[filtered_data['DEP_DELAY'] > 0]

# making a histogram to show departure delays distribution.
fig_dep_delay = px.histogram(departure_delayed_flights, x='DEP_DELAY', nbins=20, 
                             title='Departure Delays Distribution',
                             labels={'DEP_DELAY': 'Departure Delay (mins)', 'count': 'Count'}
                            )
fig_dep_delay.update_traces(marker_line=dict(color='black', width=1), 
                            hovertemplate='<b>Departure Delay:</b> %{x} mins<br><b>Count:</b> %{y}<extra></extra>')
fig_dep_delay.update_layout(barmode='overlay', hovermode='closest') 
st.plotly_chart(fig_dep_delay)


# AVERAGE DELAY FOR THE AIRPORT/AIRLINES
st.header('Average Departure Delay')
average_dep_delay = departure_delayed_flights['DEP_DELAY'].mean()
st.write(f"The average departure delay for flights departing from {selected_airport} with {selected_airline} is {average_dep_delay} minutes.")




# BUSIEST DEPARTURE TIMES
st.header(f'Busiest Departure Times Based on Selected Departure Airport and Airlines')




# converting departure time to datetime format.
flights_data['CRS_DEP_TIME'] = pd.to_datetime(flights_data['CRS_DEP_TIME'], format='%H%M', errors='coerce')

# extracting hour from departure time.
flights_data['DepHour'] = flights_data['CRS_DEP_TIME'].dt.hour

# filtering data based on user's selected airport and airline.
filtered_data = flights_data[(flights_data['ORIGIN'] == selected_airport) & (flights_data['AIRLINE'] == selected_airline)]

# counting occurrences of each departure hour.
departure_counts = filtered_data['DepHour'].value_counts().sort_index()

# making the bar chart
fig = px.bar(departure_counts, x=departure_counts.index, y=departure_counts.values,
             labels={'x': 'Departure Hour', 'y': 'Number of Flights'},
             title=f'Busiest Departure Times from {selected_airport} with {selected_airline}')

# fromatting ym x-axis to make it seem appealing.
hours = [(f'{h % 12 if h % 12 != 0 else 12} {"AM" if h < 12 else "PM"}') for h in range(24)]
fig.update_xaxes(tickvals=list(range(24)), ticktext=hours)
fig.update_layout(xaxis=dict(tickmode='array'))

# adding a tooltip.
fig.update_traces(hovertemplate='<b>Departure Hour:</b> %{x}<br><b>Number of Flights:</b> %{y}<extra></extra>')
st.plotly_chart(fig)






# renaming my columns so that I can use it later to make sure its easy for my users 
filtered_data.rename(columns={'DELAY_DUE_CARRIER': 'Carrier Delay','DELAY_DUE_WEATHER': 'Weather Delay',
                              'DELAY_DUE_NAS': 'NAS Delay','DELAY_DUE_SECURITY': 'Security Delay',
                              'DELAY_DUE_LATE_AIRCRAFT': 'Late Aircraft Delay'}, inplace=True)


st.header("Flight Status and Delay Types Distribution")

# calculating flight count for cancelled, delayed and or diverted flights.
flight_status_counts = {
    "Cancelled": filtered_data['CANCELLED'].sum(),
    "Delayed": filtered_data[filtered_data['DEP_DELAY'] > 0].shape[0],
    "Diverted": filtered_data['DIVERTED'].sum()
}

# counting delay types.
delay_counts = filtered_data[['Carrier Delay', 'Weather Delay', 'NAS Delay', 'Security Delay', 'Late Aircraft Delay']].sum()

# making the bigger pie chart with flight overall status.
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=list(flight_status_counts.keys()),
    values=list(flight_status_counts.values()),
    textinfo='label+percent', 
    hole=0.5,
    domain={"x": [0, 0.5]},
    legendgroup="Flight Status",
    showlegend=False,
    hovertemplate='<b>Flight Status:</b> %{label}<br>' + '<b>Value:</b> %{value}<br>' + '<b>Percent of Total:</b> %{percent}'))

# making a smaller pie chart for the delay types.
fig.add_trace(go.Pie(
    labels=delay_counts.index,
    values=delay_counts.values,
    hole=0.5,
    domain={"x": [0.70, 1]},
    legendgroup="Delay Types",
    hovertemplate='<b>Cause of Delay:</b> %{label}<br>' + '<b>Value:</b> %{value}<br>' + '<b>Percent of Total:</b> %{percent}'))

fig.update_layout(
    title_text="Flight Status and Delay Types Distribution",
    annotations=[{"text": "Flight Status", "x": 0.19, "y": 0.5, "showarrow": False},{"text": "Delay Types", "x": 0.91, "y": 0.5, "showarrow": False}],
    legend_title=dict(text="<b>Legend</b>") 
)
st.plotly_chart(fig, use_container_width=True)
