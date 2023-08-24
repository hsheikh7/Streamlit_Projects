import streamlit as st
import joblib
import pandas as pd
from utils import * 

# Load the pipeline from the joblib file
loaded_pipeline = joblib.load('Housing_Price_Melbourne/housing_pipeline.joblib')

# Streamlit app code
st.title("Melbourne Housing Price Prediction")

# Input form
st.sidebar.title("Input Features")
rooms = st.sidebar.number_input("Number of Rooms", value=3, min_value=1, max_value=10)
distance = st.sidebar.number_input("Distance", value=10)
bathroom = st.sidebar.number_input("Number of Bathrooms", value=2, min_value=0, max_value=10)
landsize = st.sidebar.number_input("Landsize", value=600, min_value=1, max_value=50000)
building_area = st.sidebar.number_input("Building Area", value=150, min_value=0, max_value=50000)
year_built = st.sidebar.number_input("Year Built", value=2000, min_value=1800, max_value=2020)
car = st.sidebar.number_input("Number of Car Spaces", value=2, min_value=0, max_value=10)

suburb = st.sidebar.selectbox("Suburb", suburb_options)
type = st.sidebar.selectbox("Type", ['H: House, Cottage,Villa,Semi-terrace', 'T: Townhouse, Dev-site, or other residential.', 'U: Unit, Duplex'])

regionname = st.sidebar.selectbox("Region Name", region_options)

# Create a dictionary with input data
input_data = {
    'Rooms': rooms,
    'Distance': distance,
    'Bathroom': bathroom,
    'Landsize': landsize,
    'BuildingArea': building_area,
    'YearBuilt': year_built,
    'Car': car,
    'Suburb': suburb,
    'Type': type,
    'Regionname': regionname
}

# Convert the dictionary into a DataFrame
input_df = pd.DataFrame([input_data])

# Make predictions using the loaded pipeline
predictions = loaded_pipeline.predict(input_df)
formatted_prediction = "${:,.2f}".format(predictions[0])

# Display the prediction
# st.write(f"Predicted Price: ${predictions[0]:,.2f}")
st.write(f"Predicted Price:", f"<span style='color:green; font-size:24px'>{formatted_prediction}</span>", unsafe_allow_html=True)


# Display a map based on the selected suburb and region
# st.header("Map")
st.markdown("<h2 style='font-size: 24px;'>Map of Selected Area</h2>", unsafe_allow_html=True)

latitude, longitude = get_coordinates_for_suburb(suburb)

# Create a DataFrame with the latitude and longitude data
data = pd.DataFrame({
    'latitude': [latitude],
    'longitude': [longitude]
})

st.map(data)




