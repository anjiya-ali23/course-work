import streamlit as st
import pandas as pd
from database import db

#Check login
if not st.session_state.get("logged_in"):
    st.error("Please login")
    st.stop()

st.title("IT Operations Dashboard")

#Get data from database
data = db.get_it_tickets()

if data:
    #Create DataFrame
    df = pd.DataFrame(data, columns=["ID", "Title", "Priority", "Status", "Created"])
    
    #Show simple stats
    st.write("Total tickets:", len(df))
    st.write("Open tickets:", len(df[df["Status"]=="Open"]))
    
    #Show table
    st.dataframe(df)
    
    #Simple chart
    st.bar_chart(df["Priority"].value_counts())
else:
    st.write("No data")