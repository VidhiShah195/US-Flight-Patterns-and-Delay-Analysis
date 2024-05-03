import streamlit as st
import pandas as pd
import plotly.express as px
import base64

st.set_page_config(
    page_title="Flight Delay and Cancelation Data Analysis",
    layout='wide',
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
        <h1 style="margin-left: 10px;">US Flight Delay Analysis From 2019 to 20223</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# making a gray horizontal line under my title (used just for fun).
st.markdown("<hr style='border: 1px solid #f0f0f0;'>", unsafe_allow_html=True)
st.write("The goal of this Streamlit app is to help you navigate and understand the flight patterns, specifically related to cancellations and delays from 2019 to 2023. You can slect either the 'Single Year' button below to filter by a speicific year or 'Range of Years' to filter by a range.")
st.markdown("<b>Note:</b> All of the charts on this page will change based on your selection.", unsafe_allow_html=True)


# converting 'FL_DATE' column to datetime.
flights_data['FL_DATE'] = pd.to_datetime(flights_data['FL_DATE'], format='%Y-%m-%d')

# adding a radio button to give my user an option for selecting single year or range of years and then based on their choice, add a dropdown or a range slider.
selection_mode = st.radio("Select data range:", ("Single Year", "Range of Years"))
if selection_mode == "Single Year":
    selected_year = st.selectbox("Select a year", sorted(flights_data['FL_DATE'].dt.year.unique()))
    selected_years = [selected_year]
elif selection_mode == "Range of Years":
    start_year, end_year = st.slider("Select a range of years", min_value=int(flights_data['FL_DATE'].dt.year.min()), 
    max_value=int(flights_data['FL_DATE'].dt.year.max()), value=(int(flights_data['FL_DATE'].dt.year.min()), int(flights_data['FL_DATE'].dt.year.max())), step=1)
    selected_years = list(range(start_year, end_year + 1))



# LINE CHART
st.subheader("Overall Flight Trends Across Selected Year(s)")
st.write("The line chart below shows the changes in the total number of flights over the selected year(s).")

# filtering the data frame based on the selected years.
filtered_data = flights_data[flights_data['FL_DATE'].dt.year.isin(selected_years)]

# adding a new column for month and year.
filtered_data['Month_Year'] = filtered_data['FL_DATE'].dt.strftime('%b-%Y')

# grouping by month_year and count the number of flights.
monthly_flights = filtered_data.groupby('Month_Year')['FL_NUMBER'].count().reset_index(name='TotalFlights')
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# converting Month_Year to categorical and sorting it by the month and year.
monthly_flights['Month_Year'] = pd.Categorical(monthly_flights['Month_Year'], categories=[f"{month}-{year}" for year in sorted(selected_years) for month in months], ordered=True)
monthly_flights = monthly_flights.sort_values('Month_Year')

# creating a dataframe to store the year for each row/data point.
year_data = pd.DataFrame({'Year': filtered_data['FL_DATE'].dt.year})

# plotting and adding tooltip.
fig1 = px.line(monthly_flights, x='Month_Year', y='TotalFlights', markers=True, 
              labels={'Month_Year': 'Month-Year', 'TotalFlights': 'Total Flights'},
              title=f'Total Number of Flights by Month and Year',
              hover_name='Month_Year', hover_data={'Month_Year': False, 'TotalFlights': True})
fig1.data[0].update(customdata=year_data['Year'])
fig1.update_traces(hovertemplate='<b>Month-Year:</b> %{x}<br><b>Total Flights:</b> %{y:,.0f}', line_color='#048092')
st.plotly_chart(fig1)




# BAR CHART
st.subheader(f"Weekly Overview Flight Schedule")
st.write("The bar chart below shows the total number of flights scheduled for each day of the week based on the selected year(s).")

# extracting day of the week information and then grouping the filtered data by it and total flights.
filtered_data['DayOfWeek'] = filtered_data['FL_DATE'].dt.day_name()
flights_by_day = filtered_data.groupby('DayOfWeek')['FL_NUMBER'].count().reset_index(name='TotalFlights')

# plotting the filtered data with color based on flight count (getting darker as the number of flights increase).
fig2 = px.bar(flights_by_day, x='DayOfWeek', y='TotalFlights', 
             title='Total Number of Flights by Day of the Week',
             labels={'DayOfWeek': 'Day Of Week', 'TotalFlights': 'Total Flights'})
fig2.update_xaxes(categoryorder='array', categoryarray=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
fig2.update_traces(hovertemplate='<b>Day of the Week:</b> %{label}<br><b>Total Flights:</b> %{value:,.0f}<extra></extra>', marker_color='#048092')
st.plotly_chart(fig2)





# TREE MAP WITH TOP 10 BUSIEST AIRPORTS 
st.subheader("Top 10 Busiest Airport")
st.write("The tree map below shows the top 10 busiest airports based on the selected year(s).")

# creating a dataframe with the top 10 busiest airports and putting that into a treemap. 
top_airports = filtered_data['ORIGIN'].value_counts().nlargest(10).reset_index()
top_airports.columns = ['Airport', 'Number of Flights']
fig3 = px.treemap(top_airports, path=['Airport'], values='Number of Flights', title='Top 10 Busiest Airports For Selected Years',
                  color='Number of Flights', color_continuous_scale='bluyl')
fig3.update_traces(textinfo='label+value',hovertemplate='<b>Airport:</b> %{label}<br><b>Number of Flights:</b> %{value}<extra></extra>')
fig3.update_layout(margin=dict(t=50, l=25, r=25, b=25))
st.plotly_chart(fig3)



# TOP 5 AIRLINES
st.subheader("Top 10 Airlines")
st.write("The bar chart below shows the top 5 airlines based on the number of flights for the selected year(s).")
top_airlines = filtered_data['AIRLINE'].value_counts().nlargest(10).reset_index()
top_airlines.columns = ['Airline', 'Number of Flights']
fig4 = px.bar(top_airlines, x='Airline', y='Number of Flights', 
              title='Top 5 Airlines by Number of Flights')
fig4.update_traces(hovertemplate='<b>Airline:</b> %{x}<br><b>Number of Flights:</b> %{y:,.0f}<extra></extra>', marker_color='#048092')
st.plotly_chart(fig4)




# DONUT CHART
st.subheader("Distribution of Flight Status")
st.write("The donut chart below shows the distibution in percentage of the flights that were delayed, cancelled or diverted based on the selected year(s).")

# counting delayed, diverted, and cancelled flights and then creating a dataframe with it.
delayed_count = len(filtered_data[filtered_data['ARR_DELAY'] > 0])
diverted_count = len(filtered_data[filtered_data['DIVERTED'] == 1])
cancelled_count = len(filtered_data[filtered_data['CANCELLED'] == 1])
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
st.write("The bar chart below shows the top 5 busiest airports based on your chosen delay type and previously selected year(s).")
st.write("There are five types of delays: ")
st.write("1. Carrier Delay ✈ Delay caused due to carrier, for example maintenance, crew problems, aircraft cleaning, fueling, etc.")
st.write("2. Weather Delay ✈ Delay due to extreme weather conditions.")
st.write("3. NAS Delay ✈ Delay by National Aviation System (NAS) caused due to non-extreme weather conditions, airport operations, heavy traffic volumes, air traffic control, etc.")
st.write("4. Security Delay ✈ Delay caused by security related issues, such as terminal evacuations, aircraft re-boarding due to security breaches, malfunctioning screening equipment, or long queues exceeding 29 minutes at screening areas.")
st.write("5. Late Aircraft Delay ✈ Delay due to delayed aircrafts.")

filtered_data.rename(columns={'DELAY_DUE_CARRIER': 'Carrier Delay', 'DELAY_DUE_WEATHER': 'Weather Delay',
                             'DELAY_DUE_NAS': 'NAS Delay', 'DELAY_DUE_SECURITY': 'Security Delay', 
                             'DELAY_DUE_LATE_AIRCRAFT': 'Late Aircraft Delay'}, inplace=True)

# filtering delayed flights.
delayed_flights = filtered_data[filtered_data['ARR_DELAY'] > 0]

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