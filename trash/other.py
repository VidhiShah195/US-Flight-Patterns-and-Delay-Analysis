
# LINE CHART BY MONTH ONLY
# # Convert 'Date' column to datetime with day-month-year format
# flights_data['Date'] = pd.to_datetime(flights_data['Date'], format='%d-%m-%Y')

# # Add a new column for month
# flights_data['Month'] = flights_data['Date'].dt.month

# # Group by month and count the number of flights
# monthly_flights = flights_data.groupby('Month')['FlightNum'].count().reset_index(name='TotalFlights')

# # Filter data for January to June
# monthly_flights_jan_to_jun = monthly_flights[monthly_flights['Month'].isin(range(1, 7))]

# # Plotting
# st.title('Total Number of Flights Over Time')
# st.write("The line graph below shows the total number of flights over time, grouped by the month.")

# # Interactive line plot with Plotly
# fig = px.line(monthly_flights_jan_to_jun, x='Month', y='TotalFlights', markers=True, 
#               labels={'Month': 'Month', 'TotalFlights': 'Total Flights'},
#               title='Total Number of Flights from January to June',
#               hover_name='Month', hover_data={'Month': False, 'TotalFlights': True})

# # Update hover template to display total flights as whole numbers
# fig.update_traces(hovertemplate='<b>Month:</b> %{x}<br><b>Total Flights:</b> %{y:.0f}')


# # Set x-axis range from January to June
# fig.update_xaxes(range=[0.9, 6.1], tickvals=[1, 2, 3, 4, 5, 6], ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'])

# # Show plot
# st.plotly_chart(fig)














# st.title('Filters')
# selected_airport = st.selectbox('Select Departure Airport', flights_data['Origin'].unique())
# selected_airline = st.selectbox('Select Airline', flights_data['Airline'].unique())

# filtered_data = flights_data[(flights_data['Origin'] == selected_airport) & (flights_data['Airline'] == selected_airline)]

# # st.subheader('Summary Statistics')
# # st.write(filtered_data.describe())

# # Filter delayed flights
# delayed_flights = filtered_data[filtered_data['ArrDelay'] > 0]

# # Group by destination airport and count delayed flights
# delayed_flights_count = delayed_flights.groupby('Dest_Airport').size().reset_index(name='Delayed Flights')

# # Sort by delayed flights count in descending order
# delayed_flights_count = delayed_flights_count.sort_values(by='Delayed Flights', ascending=False)

# # Plot delayed flights by destination airport
# fig = px.bar(delayed_flights_count, x='Delayed Flights', y='Dest_Airport',
#              orientation='h', title='Delayed Flights by Destination Airport',
#              labels={'Delayed Flights': 'Number of Delayed Flights', 'Dest_Airport': 'Destination Airport'},
#              template='plotly_white', opacity=0.7,
#              )
# fig.update_traces(marker_line=dict(color='black', width=1))
# st.plotly_chart(fig)












# # Convert DepTime to hh:mm format
# filtered_data['DepHour'] = filtered_data['DepTime'] // 100
# filtered_data['DepMinute'] = filtered_data['DepTime'] % 100
# filtered_data['DepHourMinute'] = filtered_data['DepHour'] + filtered_data['DepMinute'] / 60

# # Plot departure time vs arrival delay
# fig = px.scatter(filtered_data, x='DepHourMinute', y='ArrDelay', 
#                  title='Departure Time vs Arrival Delay',
#                  labels={'DepHourMinute': 'Departure Time (Hour)', 'ArrDelay': 'Arrival Delay (mins)'},
#                  template='plotly_white',
#                  hover_data={'DepHourMinute': True, 'ArrDelay': True, 'FlightNum': True, 'Dest': True}
#                 )
# fig.update_traces(marker=dict(size=8, opacity=0.7), 
#                   selector=dict(mode='markers'))
# fig.update_layout(showlegend=False)
# fig.update_xaxes(tickvals=list(range(0, 25, 2)))  # Show ticks every 2 hours
# fig.update_yaxes(range=[-100, 200])  # Limit y-axis for better visualization
# st.plotly_chart(fig)













# MAP SHOULD WORK PERFECTLY FINE WIHT NOTHING BEING SHOWN ON THE MAP AND IT NEVER LOADING
# @st.cache_data
# def load_shp_file(shp):
#     return gpd.read_file(shp)

# gdf = load_shp_file("geo_data/USA_Airports.shp")

# st.write(gdf)
# # Add a multi-select widget to choose airlines
# ['geometry'] = flight_map_data['geometry'].apply(mapping)

# # Plot the map using Plotly
# fig = px.choropleth_mapbox(
#     flight_map_selected_airlines = st.multiselect("Select Airline(s):", flights_data['Airline'].unique())

# # Filter flight data based on selected airline(s)
# filtered_flights_data = flights_data[flights_data['Airline'].isin(selected_airlines)]

# # Merge filtered flight data with shapefile data
# flight_map_data = pd.merge(filtered_flights_data, gdf, how="inner", left_on="Origin", right_on="FAA_ID")


# # Convert geometry to GeoJSON
# flight_map_datadata,
#     geojson=flight_map_data['geometry'],
#     locations=flight_map_data.index,
#     color="ArrDelay",
#     color_continuous_scale="Viridis",
#     mapbox_style="carto-positron",
#     center={"lat": 38, "lon": -98},
#     zoom=3,
#     opacity=0.5,
#     labels={"ArrDelay": "Average Arrival Delay (minutes)"},
#     hover_name="Org_Airport",
#     hover_data={"ArrDelay": True, "Org_Airport": False},
# )

# # Add scatter plot for origin and destination airports
# fig.add_trace(go.Scattermapbox(
#     lat=flight_map_data['geometry'].apply(lambda x: x['coordinates'][1]),
#     lon=flight_map_data['geometry'].apply(lambda x: x['coordinates'][0]),
#     mode='markers',
#     marker=go.scattermapbox.Marker(
#         size=10,
#         color='red',
#         opacity=0.7,
#     ),
#     text=flight_map_data['Org_Airport'],
#     hoverinfo='text'
# ))

# # Add lines connecting origin and destination airports
# for i, row in flight_map_data.iterrows():
#     fig.add_trace(go.Scattermapbox(
#         mode="lines",
#         lon=[row['geometry']['coordinates'][0], row['geometry']['coordinates'][0]],  # Origin and Destination longitude
#         lat=[row['geometry']['coordinates'][1], row['geometry']['coordinates'][1]],  # Origin and Destination latitude
#         line=go.scattermapbox.Line(
#             width=1,
#             color="blue",
#         ),
#         hoverinfo='skip',
#     ))

# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# st.plotly_chart(fig)













# IDK OTHER MAP?

# # Merge datasets based on Origin and FAA_ID
# merged_data = pd.merge(flights_data, gdf, left_on='Origin', right_on='FAA_ID', how='inner')

# # Create two select boxes for destination airport and airline
# dest_airport = st.selectbox("Select Destination Airport:", merged_data['Dest_Airport'].unique())
# airline = st.selectbox("Select Airline:", merged_data['Airline'].unique())

# # Filter data based on user selection
# filtered_data = merged_data[(merged_data['Dest_Airport'] == dest_airport) & (merged_data['Airline'] == airline)]

# # Get latitude and longitude coordinates
# avg_latitude = filtered_data['geometry'].apply(lambda point: point.y).mean()
# avg_longitude = filtered_data['geometry'].apply(lambda point: point.x).mean()

# # Create a Folium map
# m = folium.Map(location=[avg_latitude, avg_longitude], zoom_start=4)

# # Plot flight paths
# for idx, row in filtered_data.iterrows():
#     folium.Marker(location=[row['geometry'].y, row['geometry'].x], popup=row['Airline']).add_to(m)

# # Display the map
# folium_static(m)







# IDK WAS IN THE ARRIVALS FILE
# st.title('Filters')
# selected_airport = st.selectbox('Select Departure Airport', flights_data['Origin'].unique())
# selected_airline = st.selectbox('Select Airline', flights_data['Airline'].unique())

# filtered_data = flights_data[(flights_data['Origin'] == selected_airport) & (flights_data['Airline'] == selected_airline)]

# st.subheader('Summary Statistics')
# st.write(filtered_data.describe())

# # Plot arrival delays with Plotly
# st.subheader('Arrival Delays Distribution')
# fig = px.histogram(filtered_data, x='ArrDelay', nbins=20, title='Arrival Delays Distribution',
#                    labels={'ArrDelay': 'Arrival Delay (mins)', 'count': 'Count'},
#                    template='plotly_white', opacity=0.7,
#                    )
# fig.update_traces(marker_line=dict(color='black', width=1), 
#                   hovertemplate='<b>Arrival Delay:</b> %{x} mins<br><b>Count:</b> %{y}<extra></extra>')
# fig.update_layout(barmode='overlay', hovermode='closest')  # Overlay bars for better comparison
# st.plotly_chart(fig)

# average_delay = filtered_data['ArrDelay'].mean()
# st.subheader('Average Arrival Delay')
# st.write(f"The average arrival delay for flights departing from {selected_airport} with {selected_airline} is {average_delay} minutes.")


























# # BAR CHART THAT SHOWS THE TOP 10 BUSSIEST AIRPORTS
# st.header('Top 10 Busiest Airports For Departures')
# st.write("The bar chart below displays the top 10 busiest airports based on the total number of flights departing from each airport.")

# # counting the number of flights departing from each airport.
# busiest_airports = flights_data['ORIGIN'].value_counts().reset_index()
# busiest_airports.columns = ['Airport', 'TotalFlights']

# # sorting the airports by the total number of flights.
# busiest_airports = busiest_airports.sort_values(by='TotalFlights', ascending=False)

# # selecting the top 10 busiest airports.
# top_busiest_airports = busiest_airports.head(10)

# fig = px.bar(top_busiest_airports, x='Airport', y='TotalFlights', 
#              labels={'Airport': 'Airport Code', 'TotalFlights': 'Total Flights'},
#              title=f'Top 10 Busiest Airports',
#              hover_name='Airport', hover_data={'Airport': False, 'TotalFlights': True})
# fig.update_layout(xaxis_title='Airport Code', yaxis_title='Total Flights')
# fig.update_xaxes(categoryorder='total descending') 
# fig.update_yaxes(tickformat='d')
# st.plotly_chart(fig)










# # BAR CHART THAT SHOWS THE TOP 10 BUSSIEST AIRPORTS
# st.header('Top 10 Busiest Airports For Arrivals')
# st.write("The bar chart below displays the top 10 busiest airports based on the total number of flights arriving at each airport.")

# # counting the number of flights arriving at each airport.
# busiest_airports = flights_data['DEST'].value_counts().reset_index()
# busiest_airports.columns = ['Airport', 'TotalFlights']

# # sorting the airports by the total number of flights.
# busiest_airports = busiest_airports.sort_values(by='TotalFlights', ascending=False)

# # selecting the top 10 busiest airports
# top_busiest_airports = busiest_airports.head(10)

# fig = px.bar(top_busiest_airports, x='Airport', y='TotalFlights', 
#              labels={'Airport': 'Airport Code', 'TotalFlights': 'Total Flights'},
#              title=f'Top 10 Busiest Airports',
#              hover_name='Airport', hover_data={'Airport': False, 'TotalFlights': True})
# fig.update_layout(xaxis_title='Airport Code', yaxis_title='Total Flights')
# fig.update_xaxes(categoryorder='total descending') 
# fig.update_yaxes(tickformat='d')
# st.plotly_chart(fig)






# # HISTOGRAM WITH DELAYS WORKED BUT DOESN"T LOOK NICE!
#     departure_delayed_flights = filtered_data[filtered_data['DEP_DELAY'] > 0]

#     # making a histogram to show departure delays distribution.
#     fig2 = px.histogram(departure_delayed_flights, x='DEP_DELAY', nbins=30, 
#                                  title='Departure Delays Distribution',
#                                  labels={'DEP_DELAY': 'Departure Delay (mins)', 'count': 'Count'}
#                                 )
#     fig2.update_traces(marker_line=dict(color='black', width=1), 
#                                 hovertemplate='<b>Departure Delay:</b> %{x} mins<br><b>Count:</b> %{y}<extra></extra>', marker_color='#048092')
#     fig2.update_layout(barmode='overlay', hovermode='closest') 
#     st.plotly_chart(fig2)








# ARRIVALS MAP
# st.header(f'Map of {selected_airline_arr} Flights Landing in {selected_airport_arr} airport')
# st.write(f"The map below displays the origin of flights landing in {selected_airport_arr} on {selected_airline_arr}")
# st.markdown("<b>Note:</b> This map shows the total number of flights, not each individual flight, that landed with the chosen airline and originated in the city where the marker has been placed. For more infromation, click on the marker", unsafe_allow_html=True)

# # added cache for my shape file to ensure that the data doesn't have to be reloaded everytime the file runs.
# @st.cache_data
# def load_shp_file(shp):
#     return gpd.read_file(shp)

# # using the above defined function to read my shape file.
# gdf = load_shp_file("geo_data/USA_Airports.shp")

# # st.write(gdf)

# # mergeing datasets based on ORIGIN and FAA_ID.
# merged_data = pd.merge(flights_data, gdf, left_on='ORIGIN', right_on='FAA_ID', how='inner')

# # filtering data based on user's selections.
# filtered_data = merged_data[(merged_data['DEST'] == selected_airport_arr) & (merged_data['AIRLINE'] == selected_airline_arr)]

# # getting latitude and longitude for the destination airport.
# selected_dest_row = merged_data[merged_data['DEST'] == selected_airport_arr].iloc[-1]

# # creating a folium map centered at the center of US.
# m = folium.Map(location=[39.833333, -98.583333], zoom_start=4)

# # iterating over each row in the filtered_data DataFrame and adding a marker with airoplane on it at the airports with tooltips
# for idx, row in filtered_data.iterrows():
#     origin_lat = row['geometry'].y
#     origin_lon = row['geometry'].x
#     origin_airport = row['ORIGIN']
#     folium.Marker(location=[origin_lat, origin_lon],
#                   icon=folium.Icon(icon='plane', prefix='fa'),
#                   popup=f"<b>Route: </b> <br>{row['ORIGIN_CITY']}   ✈   {row['DEST_CITY']}<br>"
#                           f"<br><b>Carrier: </b> {row['AIRLINE']}<br>"
#                           f"<br> <b>Number of Flights:</b> {row['FL_NUMBER']}<br>").add_to(m)

# folium_static(m)


# # DEPARTURE MAP
# st.header(f'Map of {selected_airline_dep} Flights Departing From {selected_airport_dep} airport')
# st.write(f"The map below displays the destination of flights departing from {selected_airport_dep} on {selected_airline_dep}")
# st.markdown("<b>Note:</b> This map shows the total number of flights, not each individual flight, that departed from the chosen airline and landed in the city where the marker has been placed. For more infromation, click on the marker", unsafe_allow_html=True)
# # added cache for my shape file to ensure that the data doesn't have to be reloaded everytime the file runs.
# @st.cache_data
# def load_shp_file(shp):
#     return gpd.read_file(shp)

# # using the above defined function to read my shape file.
# gdf = load_shp_file("geo_data/USA_Airports.shp")

# # st.write(gdf)

# # mergeing datasets based on ORIGIN and FAA_ID.
# merged_data = pd.merge(flights_data, gdf, left_on='DEST', right_on='FAA_ID', how='inner')

# # filtering data based on user's selections.
# filtered_data = merged_data[(merged_data['ORIGIN'] == selected_airport_dep) & (merged_data['AIRLINE'] == selected_airline_dep)]

# # getting latitude and longitude for the destination airport.
# selected_dest_row = merged_data[merged_data['ORIGIN'] == selected_airport_dep].iloc[-1]

# # creating a folium map centered at the center of US.
# m = folium.Map(location=[39.833333, -98.583333], zoom_start=4)

# # iterating over each row in the filtered_data DataFrame and adding a marker with airoplane on it at the airports with tooltips
# for idx, row in filtered_data.iterrows():
#     dest_lat = row['geometry'].y
#     dest_lon = row['geometry'].x
#     dest_airport = row['DEST']
#     folium.Marker(location=[dest_lat, dest_lon],
#                   icon=folium.Icon(icon='plane', prefix='fa'),
#                   popup=f"<b>Route: </b> <br>{row['ORIGIN_CITY']}   ✈   {row['DEST_CITY']}<br>"
#                           f"<br><b>Carrier: </b> {row['AIRLINE']}<br>"
#                           f"<br> <b>Number of Flights:</b> {row['FL_NUMBER']}<br>").add_to(m)

# folium_static(m)















# # AVERAGE DELAY FOR THE AIRPORT/AIRLINES
# st.subheader('Overall Average Arrival Delay')

# # Extracting relevant columns
# scatter_data = filtered_data_dep[['FL_DATE', 'DEP_DELAY']]

# # Converting FL_DATE to datetime format
# scatter_data['FL_DATE'] = pd.to_datetime(scatter_data['FL_DATE'])

# # Filtering out negative departure delays
# scatter_data = scatter_data[scatter_data['DEP_DELAY'] >= 0]

# # Grouping by FL_DATE and calculating the average departure delay for each date
# scatter_data_positive_delay = scatter_data.groupby('FL_DATE')['DEP_DELAY'].mean().reset_index()

# # Calculating the average departure delay for the filtered data
# average_dep_delay = scatter_data_positive_delay['DEP_DELAY'].mean()
# # Rounding the average delay
# rounded_average = round(average_dep_delay)
# st.write(f"The average departure delay for flights departing from {selected_airport_dep} with {selected_airline_dep} is approximately {rounded_average} minutes.")













# st.subheader(f'Arrival Delays For {selected_airport_arr} with {selected_airline_arr} Over Time')

# # Extracting relevant columns
# scatter_data = filtered_data_arr[['FL_DATE', 'ARR_DELAY']]

# # Converting FL_DATE to datetime format
# scatter_data['FL_DATE'] = pd.to_datetime(scatter_data['FL_DATE'])

# # Filtering out negative arrival delays
# scatter_data = scatter_data[scatter_data['ARR_DELAY'] >= 0]

# # Grouping by FL_DATE and calculating the average arrival delay for each date
# scatter_data = scatter_data.groupby('FL_DATE')['ARR_DELAY'].mean().reset_index()

# # Making the scatter plot
# fig2 = px.scatter(scatter_data, x='FL_DATE', y='ARR_DELAY', title='Average Arrival Delay Over Time',
#                   labels={'FL_DATE': 'Date', 'ARR_DELAY': 'Average Arrival Delay (mins)'})
# fig2.update_traces(hovertemplate='<b>Date:</b> %{x}<br><b>Average Arrival Delay:</b> %{y} mins<extra></extra>', marker_color='#73C6A2')
# fig2.update(layout_coloraxis_showscale=False)
# st.plotly_chart(fig2)



# # AVERAGE DELAY FOR THE AIRPORT/AIRLINES
# st.subheader('Overall Average Arrival Delay')
# # Filtering data to include only positive delay values.
# scatter_data_positive_delay = scatter_data[scatter_data['ARR_DELAY'] > 0]
# # Calculating the average arrival delay for the filtered data
# average_arr_delay = scatter_data_positive_delay['ARR_DELAY'].mean()
# # Rounding the average delay
# rounded_average = round(average_arr_delay)
# st.write(f"The average arrival delay for flights landing in {selected_airport_arr} airport with {selected_airline_arr} is approximately {rounded_average} minutes.")



# #renaming my columns so that I can use it later to make sure its easy for my users.
# filtered_data_arr.rename(columns={'DELAY_DUE_CARRIER': 'Carrier Delay','DELAY_DUE_WEATHER': 'Weather Delay',
#                             'DELAY_DUE_NAS': 'NAS Delay','DELAY_DUE_SECURITY': 'Security Delay',
#                             'DELAY_DUE_LATE_AIRCRAFT': 'Late Aircraft Delay'}, inplace=True)

# st.subheader("Flight Status and Delay Types Distribution for Arrivals")

# # calculating flight count for cancelled, delayed, and diverted flights.
# flight_status_counts_arrival = {
#     "Cancelled": filtered_data_arr['CANCELLED'].sum(),
#     "Delayed": filtered_data_arr[filtered_data_arr['ARR_DELAY'] > 0].shape[0],
#     "Diverted": filtered_data_arr['DIVERTED'].sum()
# }

# fig3 = go.Figure()
# # making the bigger pie chart with flight overall status.
# fig3.add_trace(go.Pie(
#     labels=list(flight_status_counts_arrival.keys()),
#     values=list(flight_status_counts_arrival.values()),
#     textinfo='label+percent', 
#     hole=0.5,
#     domain={"x": [0, 0.5]},
#     legendgroup="Flight Status",
#     showlegend=False,
#     hovertemplate='<b>Flight Status:</b> %{label}<br>' + '<b>Value:</b> %{value}<br>' + '<b>Percent of Total:</b> %{percent}'))


# # Filter the data to include only rows where ARR_DELAY is positive
# pos_delay = filtered_data_arr[filtered_data_arr['ARR_DELAY'] > 0]

# # Count delay types where ARR_DELAY is positive
# delay_counts = pos_delay[['Carrier Delay', 'Weather Delay', 'NAS Delay', 'Security Delay', 'Late Aircraft Delay']].apply(lambda x: (x > 0).sum())

# # making a smaller pie chart for the delay types.
# fig3.add_trace(go.Pie(
#     labels=delay_counts.index,
#     values=delay_counts.values,
#     hole=0.5,
#     domain={"x": [0.70, 1]},
#     legendgroup="Delay Types",
#     hovertemplate='<b>Cause of Delay:</b> %{label}<br>' + '<b>Value:</b> %{value}<br>' + '<b>Percent of Total:</b> %{percent}'))
# fig3.update_layout(
#     title_text="Flight Status and Delay Types Distribution for Arrivals",
#     annotations=[{"text": "Flight Status", "x": 0.19, "y": 0.5, "showarrow": False},{"text": "Delay Types", "x": 0.91, "y": 0.5, "showarrow": False}],
#     legend_title=dict(text="<b>Legend</b>"), width=900, height=600)

# st.plotly_chart(fig3, use_container_width=True)