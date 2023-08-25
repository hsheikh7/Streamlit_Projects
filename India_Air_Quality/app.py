import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Clean Air For India')

# Add an expandable section with multiple subsections
with st.expander('More Information'):
    # Add an "About" subsection
    st.markdown('### About The Project')
    st.write('This project is an interactive visualization of air quality data for cities in India. The goal of this project is to provide an accessible and informative way for people to explore air quality data and learn more about public policies.')

    # Add a subsection on air quality in India
    st.markdown('### Air Quality in India')
    st.write('Air quality in India is a vital issue due to its severe health impacts, including respiratory diseases and increased healthcare costs, economic productivity losses, and environmental degradation. Also, India\'s commitment to global agreements and the interconnectedness of air pollution and climate change underline the urgency of improving air quality.\n\nUrbanization, industrialization, and regulatory needs demand attention. Enhancing air quality ensures better quality of life, sustains long-term development, and fosters a healthier population. Despite progress, sustained efforts are crucial to mitigate the broad spectrum of issues stemming from poor air quality.')

    # Add a subsection on the source code
    st.markdown('### Clean Air for India')
    st.write('By providing accessible air quality information, we aim to enhance awareness and create a way for people to collaborate effectively. This approach fosters informed actions, empowering individuals to collectively contribute to improving air quality and aligns with the website\'s focus on enhancing public engagement for cleaner air.')

    # Add a subsection on the source code
    st.markdown('### Source Code')
    st.write('The source code for this project is written in Python and uses the Streamlit and Plotly libraries to create a web-based user-friendly interface. The code is available on GitHub: https://github.com/hsheikh7/Streamlit_Projects.')

    # Add a subsection on the source code
    st.markdown('### Data')
    st.write('The data originates from "Air Quality Data in India (2015 - 2020)" available at: https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india?select=city_day.csv')

# Load the air quality dataset
df = pd.read_csv('India_Air_Quality/air_quality_data.csv')

# Remove rows with missing values in the date column
df = df.dropna(subset=['Date'])

# Convert the date column to a datetime object
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

# ------------- Pollutants Diagram -----------------
# Create a selectbox widget to allow the user to select the city
cities = df['City'].unique()
selected_city = st.selectbox('Select city', cities)

# Filter the data to only include rows for the selected city
df = df[df['City'] == selected_city]

# Create a multiselect widget to allow the user to select the pollutants to display
pollutants = st.multiselect('Select pollutants', ['PM2.5','PM10','NO','NO2','NOx','NH3','CO','SO2','O3','Benzene','Toluene','Xylene'])

# Create a scatter plot to display the selected pollutants over time for each city
if pollutants:
    chart_data = df.melt(id_vars=['Date', 'City'], value_vars=pollutants, var_name='pollutant', value_name='level')
    fig = px.scatter(chart_data, x='Date', y='level', color='pollutant')
    
    # Update the title of each subplot
    fig.update_layout({'xaxis1': {'title': {'text': f'Air Quality of {selected_city}'}}})
    
    st.plotly_chart(fig, width=800, height=600)
    
else:
    st.write('Please select at least one pollutant.')



# ------------- Indicators Acceptable Levels -----------------
# Create a DataFrame with the acceptable levels of various air pollutants
data = {'Pollutant': ['PM2.5','PM10','NO','NO2','NOx','NH3','CO','SO2','O3','Benzene','Toluene','Xylene'],
        'Acceptable Level': [12, 50, 53, 100, 100, 100, 9, 75, 70, 5, 7.5, 150]}
acceptable_levels = pd.DataFrame(data)

# Set the index of the acceptable_levels DataFrame to the 'Pollutant' column
acceptable_levels = acceptable_levels.set_index('Pollutant')

# Define a CSS style for centering text in a column
css_style = """
<style>
    td:nth-child(2) {
        text-align: center;
    }
</style>
"""
# Display the acceptable levels as a table without row numbers
st.markdown(f'## Level of Air Pollutants in {selected_city}')

# Group the data by city and year
grouped = df.groupby([df['City'], df['Date'].dt.year])

# Calculate the mean of each pollutant column
annual_averages = grouped[['PM2.5','PM10','NO','NO2','NOx','NH3','CO','SO2','O3','Benzene','Toluene','Xylene']].mean().round(1)

# Reset the index to move the group labels into columns
annual_averages = annual_averages.reset_index()

# Rename the 'Date' column to 'Year'
annual_averages = annual_averages.rename(columns={'Date': 'Year'})

# Melt the annual_averages DataFrame to create a long format table
long_table = annual_averages.melt(id_vars=['City', 'Year'], var_name='Pollutant', value_name='Value')

# Filter the data to only include rows for the selected city
long_table = long_table[long_table['City'] == selected_city]

# Pivot the long_table DataFrame to create a wide format table with columns for each year
pollutant_table = long_table.pivot_table(index='Pollutant', columns='Year', values='Value')

# Reindex the pollutant_table DataFrame to match the order of pollutants in the acceptable_levels DataFrame
pollutant_table = pollutant_table.reindex(acceptable_levels.index)
# Add a column for the acceptable levels
pollutant_table.insert(0, 'Acceptable Level', acceptable_levels['Acceptable Level'])

# Convert the DataFrame to an HTML table
html_table2 = pollutant_table.to_html(formatters={'Acceptable Level': '{:,.0f}'.format})
st.markdown(css_style + html_table2, unsafe_allow_html=True)


# Display the resulting table
# st.dataframe(pollutant_table)




#Map 

#Implementations - Air Quality Policies 
#About the World 
    
