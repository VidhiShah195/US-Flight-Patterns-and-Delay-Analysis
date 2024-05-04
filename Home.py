import streamlit as st
import pandas as pd
import plotly.express as px
import base64

st.set_page_config(
    page_title="Home: Flight Delay and Cancelation Data Analysis",
    page_icon='✈️'
    )

# reading the gif file as binary data and then encoding it as a base64, and storing the result as a string.
with open("data/airport.gif", "rb") as f:
    gif_data = f.read()
gif = base64.b64encode(gif_data).decode()


# creating a centrerd layout with the gif and tile being in the same line and there being 10 pixels of space between the gif and title.
st.markdown(
    f"""
    <div style="display: flex; justify-content: center; align-items: center;">
        <img src="data:image/gif;base64,{gif}" alt="gif" width="100">
        <h1 style="margin-left: 10px;">Overall US Flight Patterns From January to August 2023</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

# making a gray horizontal line under my title.
st.markdown("<hr style='border: 1px solid #f0f0f0;'>", unsafe_allow_html=True)

st.write("The goal of this Streamlit app is to help you navigate and understand the overall flight patterns, including those related to cancellations and delays from January to August of 2023. There are two additional pages which can be accessed through the side bar on the left.")


# added cache to ensure that the data doesn't have to be reloaded everytime the file runs.
@st.cache_data
def load_data(csv):
    return pd.read_csv(csv)

# reading the csv as a pandas daatframe.
flights_data = load_data("data/flights_sample_3m.csv")

# converting 'FL_DATE' column to datetime.
flights_data['FL_DATE'] = pd.to_datetime(flights_data['FL_DATE'])



# LINE CHART
st.header("Overall Flight Trends")
st.write("The line chart below shows the changes in the total number of flights from January to August of 2023.")

# adding a new column for day, month, and year.
flights_data['Day_Month_Year'] = flights_data['FL_DATE'].dt.strftime('%d-%b-%Y')

# grouping by day and count the number of flights.
daily_flights = flights_data.groupby('FL_DATE')['FL_NUMBER'].count().reset_index(name='TotalFlights')

# Resampling data to get monthly total flights
monthly_flights = flights_data.resample('M', on='FL_DATE')['FL_NUMBER'].count().reset_index(name='TotalFlights')

# Plotting and adding tooltip
fig1 = px.line(monthly_flights, x='FL_DATE', y='TotalFlights', markers=True, 
               labels={'FL_DATE': 'Date', 'TotalFlights': 'Total Flights'},
               title='Total Number of Flights by Month',
               hover_name='FL_DATE', hover_data={'FL_DATE': False, 'TotalFlights': True})
fig1.update_traces(hovertemplate='<b>Date:</b> %{x}<br><b>Total Flights:</b> %{y:,.0f}', line_color='#048092')
st.plotly_chart(fig1)

# # plotting and adding tooltip.
# fig1 = px.line(daily_flights, x='FL_DATE', y='TotalFlights', markers=True, 
#               labels={'FL_DATE': 'Date', 'TotalFlights': 'Total Flights'},
#               title='Total Number of Flights by Day',
#               hover_name='FL_DATE', hover_data={'FL_DATE': False, 'TotalFlights': True})
# fig1.update_traces(hovertemplate='<b>Date:</b> %{x}<br><b>Total Flights:</b> %{y:,.0f}', line_color='#048092')
# st.plotly_chart(fig1)



# CREATING A FILTER THEN FILTER THE DATA FOR THE PLOTS BASED ON IT
st.header("Filter Flight Data by Month(s)")
selected_month = st.selectbox("Select a Month", ['All','January', 'February', 'March', 'April', 'May', 'June', 'July', 'August'])
st.markdown("<b>*Note: </b> This selection will be used to filter all the charts below.",unsafe_allow_html=True)

# filtering the data based on the selected month where if its all, then I set it back to the original data which includes all the months and if a specific month was selected, the data is filtered accordingly for each plot.
if selected_month == 'All':
    selected_month_filtered = flights_data
    top_airports = flights_data
    top_airlines = flights_data
    filtered_status = flights_data

else:
    selected_month_index = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August'].index(selected_month) + 1
    selected_month_filtered = flights_data[flights_data['FL_DATE'].dt.month == selected_month_index]
    filtered_status = selected_month_filtered
    top_airlines = selected_month_filtered
    filtered_top_airlines =selected_month_filtered 
    top_airports = flights_data[flights_data['FL_DATE'].dt.month == selected_month_index]



# DAY OF WEEK BAR CHART
if selected_month == "All":
    st.subheader("Weekly Overview")
else:
    st.subheader(f"Weekly Overview for {selected_month}")

st.write("The bar chart below shows the total number of flights scheduled for each day of the week based on the selected month(s) of 2023.")

# extracting day of the week information and then grouping the data by it and total flights.
selected_month_filtered['DayOfWeek'] = selected_month_filtered['FL_DATE'].dt.day_name()
flights_by_day = selected_month_filtered.groupby('DayOfWeek')['FL_NUMBER'].count().reset_index(name='TotalFlights')

# plotting and adding a tool tip.
fig2 = px.bar(flights_by_day, x='DayOfWeek', y='TotalFlights', 
             title=f'Total Number of Flights by Day of the Week for {selected_month}',
             labels={'DayOfWeek': 'Day Of Week', 'TotalFlights': 'Total Flights'})
fig2.update_xaxes(categoryorder='array', categoryarray=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
fig2.update_traces(hovertemplate='<b>Day of the Week:</b> %{label}<br><b>Total Flights:</b> %{value:,.0f}<extra></extra>', marker_color='#048092')
st.plotly_chart(fig2)



# TREE MAP WITH TOP 10 BUSIEST AIRPORTS 
if selected_month == "All":
    st.subheader("Top 10 Busiest Airports")
else:
    st.subheader(f"Top 10 Busiest Airports for {selected_month}")

st.write("The tree map below shows the top 10 busiest airports based on the previously selected month(s) of 2023.")

# creating a dataframe with the top 10 busiest airports and putting that into the treemap. 
top_airports = top_airports['ORIGIN'].value_counts().nlargest(10).reset_index()
top_airports.columns = ['Airport', 'Number of Flights']

# plotting and adding a tool tip.
fig3 = px.treemap(top_airports, path=['Airport'], values='Number of Flights', title=f'Top 10 Busiest Airports for {selected_month}',
                  color='Number of Flights', color_continuous_scale='bluyl')
fig3.update_traces(textinfo='label+value', hovertemplate='<b>Airport:</b> %{label}<br><b>Number of Flights:</b> %{value}<extra></extra>')
fig3.update_layout(margin=dict(t=50, l=25, r=25, b=25))
st.plotly_chart(fig3)



# TOP 10 AIRLINES
if selected_month == "All":
    st.subheader("Top 10 Airlines")
else:
    st.subheader(f"Top 10 Airlines for {selected_month}")

st.write("The bar chart below shows the top 10 airlines based on the number of flights for the the previously selected month(s) of 2023.")

# getting the top 10 airlines for the selected month.
top_airlines_by_month = top_airlines.groupby('AIRLINE')['FL_NUMBER'].count().nlargest(10).reset_index()
top_airlines_by_month.columns = ['Airlines', 'Number of Flights']

# plotting and adding a tool tip.
fig4 = px.bar(top_airlines_by_month, x='Airlines', y='Number of Flights', 
              title=f'Top 10 Airlines by Number of Flights for {selected_month}')
fig4.update_traces(hovertemplate='<b>Airline:</b> %{x}<br><b>Number of Flights:</b> %{y:,.0f}<extra></extra>', marker_color='#048092')
st.plotly_chart(fig4)



# DONUT CHART
if selected_month == "All":
    st.subheader("Overall Distribution of Flight Status")
else:
    st.subheader(f"Distribution of Flight Status for {selected_month}")

st.write("The donut chart below shows the distribution in percentage of the flights that were on time, delayed, cancelled, or diverted for the previously selected month(s) of 2023.")

# counting delayed, diverted, and cancelled flights for the selected month.
delayed_count_selected_month = len(filtered_status[filtered_status['ARR_DELAY'] > 0])
diverted_count_selected_month = len(filtered_status[filtered_status['DIVERTED'] == 1])
cancelled_count_selected_month = len(filtered_status[filtered_status['CANCELLED'] == 1])
ontime_count_selected_month = len(filtered_status[(filtered_status['ARR_DELAY'] <= 0) & (filtered_status['DIVERTED'] == 0) & (filtered_status['CANCELLED'] == 0)])

# creating a dataframe for flight status counts.
flight_status_counts_selected_month = pd.DataFrame({'Status': ['Delayed', 'Diverted', 'Cancelled', 'On-time'],'Count': [delayed_count_selected_month, diverted_count_selected_month, cancelled_count_selected_month,ontime_count_selected_month]})

# plotting and adding a tool tip.
fig5 = px.pie(flight_status_counts_selected_month, 
                             values='Count', 
                             names='Status', 
                             hole=0.5, 
                             title=f'Distribution of Flight Status')
fig5.update_traces(textinfo='percent+label', 
                                  hovertemplate='<b>Flight Status:</b> %{label}<br><b>Total Flights:</b> %{value}')
st.plotly_chart(fig5)




# BAR CHART FOR TOP 5 AIRPORTS DUE TO SELECTED DELAY TYPES
if selected_month == "All":
    st.subheader("Top 5 Airports by Delay Type")
else:
    st.subheader(f"Top 5 Airports by Delay Type for {selected_month}")

st.write("The bar chart below shows the top 5 busiest airports based on your chosen delay type and previously selected month(s).")
st.write("There are five types of delays: ")
st.write("1. Carrier Delay ✈ Delay caused due to carrier, for example maintenance, crew problems, aircraft cleaning, fueling, etc.")
st.write("2. Weather Delay ✈ Delay due to extreme weather conditions.")
st.write("3. NAS Delay ✈ Delay by National Aviation System (NAS) caused due to non-extreme weather conditions, airport operations, heavy traffic volumes, air traffic control, etc.")
st.write("4. Security Delay ✈ Delay caused by security related issues, such as terminal evacuations, aircraft re-boarding due to security breaches, malfunctioning screening equipment, or long queues exceeding 29 minutes at screening areas.")
st.write("5. Late Aircraft Delay ✈ Delay due to delayed aircrafts.")

# renaming my columns for clarity and to increase the readability in my plot.
flights_data.rename(columns={'DELAY_DUE_CARRIER': 'Carrier Delay', 'DELAY_DUE_WEATHER': 'Weather Delay',
                             'DELAY_DUE_NAS': 'NAS Delay', 'DELAY_DUE_SECURITY': 'Security Delay', 
                             'DELAY_DUE_LATE_AIRCRAFT': 'Late Aircraft Delay'}, inplace=True)

# filtering delayed flights. 
delayed_flights = flights_data[flights_data['ARR_DELAY'] > 0]

# once again filtering delayed_flights data for the selected month.
if selected_month == 'All':
    delayed_flights_selected_month = delayed_flights
else:
    selected_month_index = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August'].index(selected_month) + 1
    delayed_flights_selected_month = delayed_flights[delayed_flights['FL_DATE'].dt.month == selected_month_index]

# creating a list of reasons for delay and then add a select box to choose from the list.
delay_reasons = ['Carrier Delay', 'Weather Delay', 'NAS Delay', 'Security Delay', 'Late Aircraft Delay']
selected_reason = st.selectbox("Select Reason for Delay:", delay_reasons)

# filtering the data based on selected delay reason.
if selected_reason != 'Late Aircraft Delay':  
    delayed_flights_selected_month = delayed_flights_selected_month[delayed_flights_selected_month[selected_reason] > 0]

# counting delayed flights by airport.
delayed_by_airport_selected_month = delayed_flights_selected_month.groupby('DEST')['FL_NUMBER'].count().reset_index()
delayed_by_airport_selected_month.columns = ['Airport', 'DelayedFlights']

# sorting and selecting top 5 airports
delayed_by_airport_sorted_selected_month = delayed_by_airport_selected_month.sort_values(by='DelayedFlights', ascending=False)
top_5_airports_selected_month = delayed_by_airport_sorted_selected_month.head(5)
top_5_airports_sorted_selected_month = top_5_airports_selected_month.sort_values(by='DelayedFlights', ascending=True)

# make the horizontal bar chart for the top 5 airports with a tool tip.
fig6 = px.bar(top_5_airports_sorted_selected_month, y='Airport', x='DelayedFlights',
             title=f'Top 5 Airports with the Highest Number of Delayed Flights due to {selected_reason}',
             labels={'Airport': 'Airport Code', 'DelayedFlights': 'Number of Delayed Flights'},
             orientation='h')
fig6.update_traces(hovertemplate='<b>Airport:</b> %{y}<br><b>Number of Delayed Flights:</b> %{x:,.0f}<extra></extra>', marker_color='#048092')
st.plotly_chart(fig6)