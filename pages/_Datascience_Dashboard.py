import streamlit as st
import pandas as pd
from database import db

#Checking if user login
if not st.session_state.get("logged_in"):
    st.error("Please login")
    st.stop()

st.title("Data Science Dashboard")

#Geting data from database
data = db.get_datasets()

if data:
    #Creating a DataFrame
    df = pd.DataFrame(data, columns=["ID", "Name", "Category", "Source", "Size"])
    
    #Showing simple stats
    st.write("Total datasets:", len(df))
    st.write("Total size:", df["Size"].sum(), "MB")
    
    #Showing table
    st.dataframe(df)
    
    #creating a simple chart
    st.bar_chart(df["Category"].value_counts())
else:
    st.write("No data")