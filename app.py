import streamlit as st

st.title("Multi-Domain Platform")
st.write("Go to login page")

if st.button("Login"):
    st.switch_page("pages/Login.py")