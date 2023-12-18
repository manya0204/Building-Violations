"""
Name:       Manya Yadav
CS230:      Section 6
Data:       Boston Building Violations
URL:        Link to your web application on Streamlit Cloud (if posted)

Description:
Which buildings in Boston are unsafe to enter? This application visualizes the data researched by
Boston's Inspectional Services Department about Building Violations using charts, graphs and data analysis tools.
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
import plotly.express as px
from streamlit_folium import folium_static
import base64

# Read the Data Sheet
df = pd.read_csv(r"C:\Users\Manya Yadav\OneDrive - Bentley University\Desktop\CS 230"
                 r"\WebApp\boston_building_violations_7000_sample.csv")

# Format the Entire Page
st.set_page_config(page_title="Building Violations", page_icon="🏢", layout="wide", initial_sidebar_state="expanded")

# GIF
st.markdown("""<div style="text-align: center"><img src="https://media.giphy.com/media/2dmiD02aM9zX3Gw2oS/giphy.gif" 
                alt="Alt Text"></div>""", unsafe_allow_html=True)

# Title
st.markdown("""<h1 style='text-align: center; color: skyblue; white-space: nowrap; 
font-family: "Times New Roman", Times, serif;'>Boston Building Violations</h1>""", unsafe_allow_html=True)

# Description of the program
st.write("*This application visualizes the data researched by Boston's Inspectional Services Department about Building "
         "Violations using charts, graphs and data analysis tools.*")
st.divider()

# Sidebar Information
st.markdown("""<h2 style='text-align: left; color: gold; white-space: nowrap;font-family: "Times New Roman", 
Times, serif;'>Data Overview</h2>""", unsafe_allow_html=True)

st.sidebar.markdown("""<h2 style='text-align: left; color: pink; white-space: nowrap;font-family: "Times New Roman", 
Times, serif;'>Data Overview</h2>""", unsafe_allow_html=True)

st.markdown("""<style>h1, h2, h3, h4, h5, h6, p, .stRadio > label {font-family: 'Times New Roman', Times, serif;}
</style>""", unsafe_allow_html=True)

tabs = ['Raw Data', 'Data Analysis', 'Overview Map']
selected_tab = st.sidebar.radio('Select which data set you would like to see:', tabs)

if selected_tab == 'Raw Data':
    st.markdown("<h3 style='font-family:Times New Roman, serif;'>Raw Data</h3>", unsafe_allow_html=True)
    st.write(df)
    st.write("[This table contains all the information found in the dataset]")

elif selected_tab == 'Data Analysis':
    data_frame = df.copy()
    st.markdown("<h3 style='font-family:Times New Roman, serif;'>Analysis of the Dataset</h3>", unsafe_allow_html=True)
    st.write(data_frame.drop('value', axis=1).describe())
    st.write("[This table contains a statistical analysis of the numerical elements of the dataset]")

elif selected_tab == 'Overview Map':
    st.markdown("<h3 style='font-family:Times New Roman, serif;'>Violation Locations Map</h3>", unsafe_allow_html=True)
    st.map(df)
    st.write("[This map shows all the locations which have a property violation]")
st.divider()

# City Map
st.markdown("<h2 style='text-align: left; color:skyblue; white-space: nowrap;'>Where are the building violations?</h1>",
            unsafe_allow_html=True)
choice = st.selectbox("Select a Violation City", df["violation_city"].unique())


def create_map(city):
    fil_df = df[df["violation_city"] == city]
    center_lat = fil_df["latitude"].mean()
    center_lon = fil_df["longitude"].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

    for _, row in fil_df.iterrows():
        location = [row["latitude"], row["longitude"]]
        popup_text = f"{row['violation_street']}, {row['violation_stno']}"
        tooltip_text = f"Description of Violation:{ row['description']} | Zipcode:{row['violation_zip']}"
        folium.Marker(location=location, popup=folium.Popup(popup_text, parse_html=True), tooltip=tooltip_text,
                      icon=folium.Icon(color="red", icon="info-sign")).add_to(m)
    return m


map_object = create_map(choice)
folium_static(map_object)
st.write("[This map filters by a specific city and shows the buildings in the city which have a violation submitted. "
         "If you hover over each location, you can see the description of the violation and its zipcode]")
st.divider()

# Zipcode
df['status_dttm'] = df['status_dttm'].replace('', pd.NaT)
df['status_dttm'] = pd.to_datetime(df['status_dttm'], errors='coerce')
st.markdown("<h2 style='text-align: left; color:gold; white-space: nowrap;'>Contact Details based on Violation "
            "Zipcode</h1>", unsafe_allow_html=True)
st.write("[This filter shows the contact details such as contact address, contact city, contact zipcode and ward "
         "for buildings with a violation using the zip code found from the map above]")
zipcode_input = st.text_input("Enter Violation Zip Code:")
if zipcode_input:
    filtered_df = df[df["violation_zip"].astype(str).str.contains(zipcode_input, case=False)]
    if not filtered_df.empty:
        st.write("Contact Address:", filtered_df['contact_addr1'].iloc[0])
        st.write("Contact City:", filtered_df['contact_city'].iloc[0])
        st.write("Contact Zipcode:", filtered_df['contact_zip'].iloc[0])
        st.write("Ward:", filtered_df['ward'].iloc[0])
    else:
        st.warning(f"No data found for the Zip Code: {zipcode_input}")

st.divider()

# Slider
st.markdown("""<h2 style='text-align: left; color:skyblue; white-space: nowrap;'>Building Violations Cases based on
            Ward numbers</h2>""", unsafe_allow_html=True)
st.write("[This filter shows the violation case number based on the ward numbers]")
ward_number = st.slider("Select a Ward Number", 1, 22, 1)
filtered_df = df[df['ward'] == ward_number]
if not filtered_df.empty:
    st.write(f"Case Numbers for Ward {ward_number}:")
    st.write(filtered_df['case_no'])
else:
    st.write(f"No cases found for Ward {ward_number}.")
st.divider()

# Data filtered based on Case Number
st.sidebar.divider()
st.sidebar.markdown("""<h2 style='text-align: left; color: pink; white-space: nowrap;font-family: "Times New Roman", 
Times, serif;'>Case Specific Information</h2>""", unsafe_allow_html=True)
case_no = st.sidebar.selectbox("Select a Case Number", df['case_no'].unique())
case_details = df[df['case_no'] == case_no].iloc[0]
if case_details['status'].startswith('O'):
    st.sidebar.success(f"Case Status: {case_details['status']}\n\nDescription: {case_details['description']}"
                       f"\n\nStreet Name: {case_details['violation_street']}")
else:
    st.sidebar.error(f"Case Status: {case_details['status']}\n\nDescription: {case_details['description']}\n"
                     f"\nStreet Name: {case_details['violation_street']}")

# Image & description side by side in the sidebar
st.sidebar.divider()


def get_image_as_base64(url):
    with open(url, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


image_path = 'WebApp/ISD.png'
image_as_base64 = get_image_as_base64(image_path)

st.sidebar.markdown(f"""<div style='display: flex; align-items: center;'><img src='data:image/png;base64,
{image_as_base64}' alt='ISD' style='display: block; max-width: 100px; max-height: 100px; margin-right: 10px;'>
<div style='font-family: "Times New Roman", Times, serif;'>Data published by Inspectional Services Department</div>
</div>""", unsafe_allow_html=True)

# Filter based on cities and status
st.markdown("""<h2 style='text-align: left; color:gold; white-space: nowrap;'>Building Violations based on multiple
            cities and status</h1>""", unsafe_allow_html=True)
st.write("[You can filter by different cities and choose their status to see the building violations in those areas]")
selected_cities = st.multiselect("Select Violation Cities", options=df["violation_city"].unique())
selected_status = st.radio("Select Status", options=df["status"].unique())
filtered_df = df[df["violation_city"].isin(selected_cities) & (df["status"] == selected_status)]
if selected_cities and selected_status:
    st.write(f"Cases filtered by cities: {', '.join(selected_cities)} and status: {selected_status}")
    st.dataframe(filtered_df)
else:
    st.write("Please select at least one city and a status to see the cases.")

# Bar chart
st.divider()
st.markdown("<h1 style='text-align: left; color:skyblue; white-space: nowrap;'>Data Analysis</h1>",
            unsafe_allow_html=True)
st.markdown("<h2 style='text-align: left; color:gold; white-space: nowrap;'>Building Violations over the years</h1>",
            unsafe_allow_html=True)
st.write("[This graph shows the increase and decrease of Building violations]")
fig = px.bar(df, x='status_dttm', y='code', title='Number of Building Violations/Year', labels={'code': 'Count',
                                                                                                'status_dttm':
                                                                                                    'Status'},
             hover_data=['description'])
st.plotly_chart(fig)
st.divider()

st.markdown("<h2 style='text-align: left; color:skyblue; white-space: nowrap;"
            "'>Number of Building Violations in each city"
            "</h1>", unsafe_allow_html=True)
st.write("[This graph shows the count of building violations in each city compared to one another]")
violation_city_counts = df['violation_city'].value_counts()
st.bar_chart(violation_city_counts)
st.divider()

# Pie chart for the status of building violations
st.markdown("<h2 style='text-align: left; color:gold; white-space: nowrap;'>Status about the building "
            "violations</h1>", unsafe_allow_html=True)

status_count = df['status'].value_counts()
st.write("[In this graph, you can see the percentage of status of the building violations]")
fig, ax = plt.subplots()
ax.pie(status_count, startangle=90, autopct='%1.1f%%')
ax.legend(status_count.index, title="Status of the Building Violations", loc="center left", bbox_to_anchor=(1, 0.5))
ax.axis('equal')
st.pyplot(fig)
st.divider()

# Summary Statistics
total_cases = len(df)
open_cases = len(df[df['status'] == 'Open'])
closed_cases = len(df[df['status'] == 'Closed'])
average_value = df['value'].mean()
st.markdown("<h1 style='text-align: left; color:skyblue; white-space: nowrap;'>Summary Statistics</h1>",
            unsafe_allow_html=True)
st.write(f'Total Cases: {total_cases}')
st.write(f'Open Cases: {open_cases}')
st.write(f'Closed Cases: {closed_cases}')

st.markdown("<h2 style='text-align: left; color:gold; white-space: nowrap;'>General Statistics</h2>",
            unsafe_allow_html=True)
st.write(df.describe())

st.markdown("<h2 style='text-align: left; color:skyblue; white-space: nowrap;'>Status of Violations</h2>",
            unsafe_allow_html=True)
status_counts = df['status'].value_counts()
st.bar_chart(status_counts)