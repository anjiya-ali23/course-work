import streamlit as st
import pandas as pd
from database import DatabaseManager

#Checking if  user logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first")
    st.stop()

#Geting users domain
if st.session_state.domain != "cybersecurity":
    st.error("This is for Cybersecurity analysts only")
    st.stop()

#Initializing database
db = DatabaseManager()

#Title
st.title("Cybersecurity Dashboard")

#Geting data from database
incidents = db.get_cyber_incidents()
df = pd.DataFrame(incidents)

#Showing basic metrics
st.write(f"Total incidents: {len(df)}")
st.write(f"Open incidents: {len(df[df['status'] == 'Open'])}")

#Showing table
st.dataframe(df)

#creating a simple bar chart
st.bar_chart(df['category'].value_counts())