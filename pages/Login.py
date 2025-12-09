import streamlit as st
from database import DatabaseManager

#Initializing database
db = DatabaseManager()

#Checking if user is already logged in
if "logged_in" in st.session_state and st.session_state.logged_in:
    # Redirect to dashboard based on their domain
    st.switch_page("pages/2_Cybersecurity_Dashboard.py")

#Login form
st.title("Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    # Checking credentials
    user = db.get_user(username)
    if user and user["password_hash"] == password:  
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.domain = user["domain"]
        st.success("Logged in")
        st.rerun()
    else:
        st.error("Wrong username or password")