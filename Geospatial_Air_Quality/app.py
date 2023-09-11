import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
# import numpy as np
# from sklearn.preprocessing import LabelEncoder

# ----------- Setup the Data Table -----------

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    data = pd.read_csv('Geospatial_Air_Quality/air_quality_data.csv')
    data['Date'] = pd.to_datetime(data['Date'], format='%m/%d/%Y').dt.date
    # le = LabelEncoder()
    # data['City_Encoded'] = le.fit_transform(data['City'])
    return data

city_coordinates = pd.read_csv('Geospatial_Air_Quality/city_coordinates.csv')

def merge_data():
    air_quality_data = load_data()
    merged_data = pd.merge(air_quality_data, city_coordinates, on='City', how='left')
    return merged_data

# ----------- Create a Streamlit app -----------
st.title('Air Quality Spatial Analysis')

# Filter the dataset by year
df = merge_data()  

# Sidebar for selecting date and pollutant
st.sidebar.subheader('Filter Data')
min_date = df['Date'].min()
max_date = df['Date'].max()
selected_date = st.slider('Select Date', min_date, max_date, min_date)
selected_pollutant = st.sidebar.selectbox('Select Pollutant', ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene'])

with st.sidebar.expander('More Information'):
    # Add an "About" subsection
    st.markdown('### About The Project')
    st.write('This project is an interactive visualization of air quality data for cities in India.')

    # Add a subsection on air quality in India
    st.markdown('### Air Quality in India')
    st.write('Air quality in India is a vital issue due to its severe health impacts, economic productivity losses and environmental degradation.')

    # Add a subsection on the source code
    st.markdown('### Clean Air for India')
    st.write('By providing accessible air quality information, I aim to enhance awareness and create a way for people to collaborate effectively.')

    # Add a subsection on the source code
    st.markdown('### Source Code')
    st.write('The code is available on GitHub: https://github.com/hsheikh7/Streamlit_Projects.')

    # Add a subsection on the source code
    st.markdown('### Data')
    st.write('The data originates from "Air Quality Data in India (2015 - 2020)" available at: https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india?select=city_day.csv')


filtered_df = df[(df['Date'] == selected_date) & ~df[selected_pollutant].isna()]

city_row = df.iloc[0]  # You can choose any city as the default center
m = folium.Map(location=[city_row['Latitude'], city_row['Longitude']], zoom_start=5)


pollutants = ["PM2.5", "PM10", "NO", "NO2", "NOx", "NH3", "CO", "SO2", "O3", "Benzene", "Toluene", "Xylene"]
limits = [
    12,   # PM2.5
    20,   # PM10
    40,   # NO
    40,   # NO2
    50,   # NOx
    100,  # NH3
    4.5,  # CO
    40,   # SO2
    100,  # O3
    5,    # Benzene
    10,   # Toluene
    10    # Xylene
]

limits_df = pd.DataFrame({
    "Pollutant": pollutants,
    "Limit_of_Acceptance": limits
})

# Marker color based on pollutant value and limit
def get_marker_color(pollutant_value, limit):
    if pollutant_value <= limit:
        return 'green'
    else:
        return 'red'

# Add markers for each city to the map
for index, row in filtered_df.iterrows():
    marker_color = get_marker_color(row[selected_pollutant], limits_df.loc[limits_df['Pollutant'] == selected_pollutant, 'Limit_of_Acceptance'].values[0])
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        color=marker_color,
        fill=True,
        fill_color=marker_color,
        fill_opacity=0.7,
        tooltip=f"{row['City']}: {row[selected_pollutant]}"
    ).add_to(m)

# Display the map 
st.subheader('Air Quality Map')
folium_static(m)

# Display the filtered data in a table
st.subheader('Presented Data')
st.dataframe(filtered_df)

