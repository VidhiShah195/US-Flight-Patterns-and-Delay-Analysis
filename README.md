# US Flight Data Analysis From January to August 2023
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://us-flight-delay-analysis-twjtaq58hmjcuh6aptdaxc.streamlit.app/)

## Introduction
In today's bustling world of air travel, understanding the intricacies of flight patterns can be as challenging as navigating the skies themselves. While data on flight schedules, cancellations, and delays is readily available, making sense of this wealth of information poses its own set of hurdles. That's where my Streamlit app comes in. My app is your go-to tool for unraveling the mysteries of air travel trends in the United States from January to August of 2023. It app aims to shed light on the overarching information hidden within the data through a series of intuitive visualizations.

This app has three pages:
* **Home:** This page offers an overview of flight activity trends. Users can explore interactive line charts to examine overall flight trends or focus on specific airlines. They can also analyze flight data by selecting specific months and explore the impact of delays on air travel, highlighting the top 5 airports affected by various delay types.
* **Departures:** This page allows users to customize their analysis by selecting specific airlines and departure airports. They can explore departure patterns, peak departure hours, and flight status distributions (on-time, delays, cancellations). Additionally, users can delve into average delay times caused by different delay types to understand their impact on departure schedules.
* **Arrivals:** Similar to the Departures page, the Arrivals page allows users to customize their analysis by selecting specific airlines and arrival airports. They can explore arrival patterns, peak arrival hours, and flight status distributions. Users can also analyze average delay times caused by different delay types to understand their impact on arrival schedules.

     
## Data Sources
The Airline Flight Delay and Cancellation dataset sourced from the US Department of Transportation's (DOT) Bureau of Transportation Statistics was used as it was available on [Kaggle](https://www.kaggle.com/datasets/patrickzel/flight-delay-and-cancellation-dataset-2019-2023/data). The original dataset includes data that spans from January 2019 to August 2023, however for this project, I decided to focus solely on the data from January 2023 to August 2023 since it's the most recent and available for use. 


## Future Work
For future work, the app could integrate real-time flight data, offering users immediate updates on flight statuses, delays, and cancellations. This addition would significantly augment the app's usefulness for both travelers and industry professionals seeking the latest flight information. Moreover, implementing predictive models based on historical data patterns could enable the app to forecast potential flight delays or cancellations. To further enhance user experience, incorporating geographical visualizations to illustrate flight routes and regional performance variations could also be very useful. 
