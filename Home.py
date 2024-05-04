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
        <h1 style="margin-left: 10px;">Overall US Flight Patterns From January to August 2023</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# making a gray horizontal line under my title (used just for fun).
st.markdown("<hr style='border: 1px solid #f0f0f0;'>", unsafe_allow_html=True)
st.write("The goal of this Streamlit app is to help you navigate and understand the overall flight patterns, including those related to cancellations and delays from January to August of 2023.")

# converting 'FL_DATE' column to datetime.
flights_data['FL_DATE'] = pd.to_datetime(flights_data['FL_DATE'])



# LINE CHART
st.header("Overall Flight Trends")
st.write("The line chart below shows the changes in the total number of flights from January to August of 2023.")

# adding a new column for day, month, and year
flights_data['Day_Month_Year'] = flights_data['FL_DATE'].dt.strftime('%d-%b-%Y')

# grouping by day and count the number of flights
daily_flights = flights_data.groupby('FL_DATE')['FL_NUMBER'].count().reset_index(name='TotalFlights')

# Convert 'FL_DATE' to datetime format
daily_flights['FL_DATE'] = pd.to_datetime(daily_flights['FL_DATE'])

# plotting and adding tooltip
fig2 = px.line(daily_flights, x='FL_DATE', y='TotalFlights', markers=True, 
              labels={'FL_DATE': 'Date', 'TotalFlights': 'Total Flights'},
              title='Total Number of Flights by Day',
              hover_name='FL_DATE', hover_data={'FL_DATE': False, 'TotalFlights': True})
fig2.update_traces(hovertemplate='<b>Date:</b> %{x}<br><b>Total Flights:</b> %{y:,.0f}', line_color='#048092')
st.plotly_chart(fig2)



st.header("Filter Flight Data by Month")
selected_month = st.selectbox("Select a Month", ['All','January', 'February', 'March', 'April', 'May', 'June', 'July', 'August'])
st.markdown("<b>*Note: </b> This selection will be used to filter all the charts below.",unsafe_allow_html=True)



# BAR CHART
st.subheader("Weekly Overview")
st.write("The bar chart below shows the total number of flights scheduled for each day of the week based on the selected month(s) of 2023.")
# filtering the data based on the selected month wher if its all, then I set it back to the original data which includes all the months.
if selected_month == 'All':
    flights_data_selected_month = flights_data
else:
    selected_month_index = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August'].index(selected_month) + 1
    flights_data_selected_month = flights_data[flights_data['FL_DATE'].dt.month == selected_month_index]

# extracting day of the week information and then grouping the data by it and total flights.
flights_data_selected_month['DayOfWeek'] = flights_data_selected_month['FL_DATE'].dt.day_name()
flights_by_day = flights_data_selected_month.groupby('DayOfWeek')['FL_NUMBER'].count().reset_index(name='TotalFlights')

# plotting the data with color based on flight count (getting darker as the number of flights increase).
fig2 = px.bar(flights_by_day, x='DayOfWeek', y='TotalFlights', 
             title=f'Total Number of Flights by Day of the Week for {selected_month}',
             labels={'DayOfWeek': 'Day Of Week', 'TotalFlights': 'Total Flights'})
fig2.update_xaxes(categoryorder='array', categoryarray=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
fig2.update_traces(hovertemplate='<b>Day of the Week:</b> %{label}<br><b>Total Flights:</b> %{value:,.0f}<extra></extra>', marker_color='#048092')
st.plotly_chart(fig2)



# TREE MAP WITH TOP 10 BUSIEST AIRPORTS 
st.subheader(f"Top 10 Busiest Airport of {selected_month}")
st.write("The tree map below shows the top 10 busiest airports based on the previously selected month(s) of 2023.")
if selected_month == 'All':
    top_airports_data = flights_data
else:
    selected_month_index = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August'].index(selected_month) + 1
    top_airports_data = flights_data[flights_data['FL_DATE'].dt.month == selected_month_index]
# creating a dataframe with the top 10 busiest airports and putting that into the treemap. 
top_airports = top_airports_data['ORIGIN'].value_counts().nlargest(10).reset_index()
top_airports.columns = ['Airport', 'Number of Flights']
fig3 = px.treemap(top_airports, path=['Airport'], values='Number of Flights', title=f'Top 10 Busiest Airports for {selected_month}',
                  color='Number of Flights', color_continuous_scale='bluyl')
fig3.update_traces(textinfo='label+value', hovertemplate='<b>Airport:</b> %{label}<br><b>Number of Flights:</b> %{value}<extra></extra>')
fig3.update_layout(margin=dict(t=50, l=25, r=25, b=25))
st.plotly_chart(fig3)



# TOP 10 AIRLINES
st.subheader(f"Top 10 Airlines of {selected_month}")
st.write("The bar chart below shows the top 10 airlines based on the number of flights for the the previously selected month(s) of 2023.")
if selected_month == 'All':
    flights_data_selected_month_top_airlines = flights_data
else:
    flights_data_selected_month_top_airlines = flights_data_selected_month

# Get the top 10 airlines for the selected month
top_airlines_selected_month = flights_data_selected_month_top_airlines.groupby('AIRLINE')['FL_NUMBER'].count().nlargest(10).reset_index()
top_airlines_selected_month.columns = ['Airlines', 'Number of Flights']

# Plot the bar chart for top 10 airlines by the selected month
fig4_selected_month = px.bar(top_airlines_selected_month, x='Airlines', y='Number of Flights', 
              title=f'Top 10 Airlines by Number of Flights for {selected_month}')
fig4_selected_month.update_traces(hovertemplate='<b>Airline:</b> %{x}<br><b>Number of Flights:</b> %{y:,.0f}<extra></extra>', marker_color='#048092')
st.plotly_chart(fig4_selected_month)



# DONUT CHART
st.subheader(f"Distribution of Flight Status for {selected_month}")
st.write("The donut chart below shows the distribution in percentage of the flights that were on time, delayed, cancelled, or diverted for the previously selected month(s) of 2023.")

# Filter data for the selected month
if selected_month == 'All':
    flights_data_selected_month_status = flights_data
else:
    flights_data_selected_month_status = flights_data_selected_month

# Count delayed, diverted, and cancelled flights for the selected month
delayed_count_selected_month = len(flights_data_selected_month_status[flights_data_selected_month_status['ARR_DELAY'] > 0])
diverted_count_selected_month = len(flights_data_selected_month_status[flights_data_selected_month_status['DIVERTED'] == 1])
cancelled_count_selected_month = len(flights_data_selected_month_status[flights_data_selected_month_status['CANCELLED'] == 1])
ontime_count_selected_month = len(flights_data_selected_month_status[(flights_data_selected_month_status['ARR_DELAY'] <= 0) & (flights_data_selected_month_status['DIVERTED'] == 0) & (flights_data_selected_month_status['CANCELLED'] == 0)])

# Create a DataFrame for flight status counts
flight_status_counts_selected_month = pd.DataFrame({'Status': ['Delayed', 'Diverted', 'Cancelled', 'On-time'],'Count': [delayed_count_selected_month, diverted_count_selected_month, cancelled_count_selected_month,ontime_count_selected_month]})

# Create the donut chart for the selected month
fig5_selected_month = px.pie(flight_status_counts_selected_month, values='Count', names='Status', hole=0.5, title=f'Distribution of Flight Status')
fig5_selected_month.update_traces(textinfo='percent+label', hovertemplate='<b>Flight Status:</b> %{label}<br><b>Total Flights:</b> %{value}')
st.plotly_chart(fig5_selected_month)



# BAR CHART FOR TOP 5 AIRPORTS DUE TO SELECTED DELAY TYPES
st.subheader(f'Top 5 Airports by Delay Type for {selected_month}')
st.write("The bar chart below shows the top 5 busiest airports based on your chosen delay type and previously selected month(s).")
st.write("There are five types of delays: ")
st.write("1. Carrier Delay ✈ Delay caused due to carrier, for example maintenance, crew problems, aircraft cleaning, fueling, etc.")
st.write("2. Weather Delay ✈ Delay due to extreme weather conditions.")
st.write("3. NAS Delay ✈ Delay by National Aviation System (NAS) caused due to non-extreme weather conditions, airport operations, heavy traffic volumes, air traffic control, etc.")
st.write("4. Security Delay ✈ Delay caused by security related issues, such as terminal evacuations, aircraft re-boarding due to security breaches, malfunctioning screening equipment, or long queues exceeding 29 minutes at screening areas.")
st.write("5. Late Aircraft Delay ✈ Delay due to delayed aircrafts.")

flights_data.rename(columns={'DELAY_DUE_CARRIER': 'Carrier Delay', 'DELAY_DUE_WEATHER': 'Weather Delay',
                             'DELAY_DUE_NAS': 'NAS Delay', 'DELAY_DUE_SECURITY': 'Security Delay', 
                             'DELAY_DUE_LATE_AIRCRAFT': 'Late Aircraft Delay'}, inplace=True)

# filtering delayed flights. 
delayed_flights = flights_data[flights_data['ARR_DELAY'] > 0]

# Filter data for the selected month
if selected_month == 'All':
    delayed_flights_selected_month = delayed_flights
else:
    delayed_flights_selected_month = delayed_flights[delayed_flights['FL_DATE'].dt.month == selected_month_index]

# Create a list of reasons for delay and then add a select box to choose from the list
delay_reasons = ['Carrier Delay', 'Weather Delay', 'NAS Delay', 'Security Delay', 'Late Aircraft Delay']
selected_reason = st.selectbox("Select Reason for Delay:", delay_reasons)

# Filter data based on selected delay reason
if selected_reason != 'Late Aircraft Delay':  
    delayed_flights_selected_month = delayed_flights_selected_month[delayed_flights_selected_month[selected_reason] > 0]

# Count delayed flights by airport
delayed_by_airport_selected_month = delayed_flights_selected_month.groupby('DEST')['FL_NUMBER'].count().reset_index()
delayed_by_airport_selected_month.columns = ['Airport', 'DelayedFlights']

# Sort and select top 5 airports by the number of delayed flights
delayed_by_airport_sorted_selected_month = delayed_by_airport_selected_month.sort_values(by='DelayedFlights', ascending=False)
top_5_airports_selected_month = delayed_by_airport_sorted_selected_month.head(5)
top_5_airports_sorted_selected_month = top_5_airports_selected_month.sort_values(by='DelayedFlights', ascending=True)

# Make the horizontal bar chart for the top 5 airports
fig6_selected_month = px.bar(top_5_airports_sorted_selected_month, y='Airport', x='DelayedFlights',
             title=f'Top 5 Airports with the Highest Number of Delayed Flights due to {selected_reason}',
             labels={'Airport': 'Airport Code', 'DelayedFlights': 'Number of Delayed Flights'},
             orientation='h')
fig6_selected_month.update_traces(hovertemplate='<b>Airport:</b> %{y}<br><b>Number of Delayed Flights:</b> %{x:,.0f}<extra></extra>', marker_color='#048092')
st.plotly_chart(fig6_selected_month)