# chat.py shows AI Chat page
import streamlit as st
import google.generativeai as genai

#geting API key
genai.configure(api_key=st.secrets["AIzaSyBwx232DAcgGcsqaKCI5YLfdsLTW9Jx3Zw"])

#using working model change if needed
model = genai.GenerativeModel("gemini-1.5-flash-latest")

st.title(" AI Chat Assistant")

#storing messages
if "messages" not in st.session_state:
    st.session_state.messages = []

#showing old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

#geting user input
user_input = st.chat_input("Type your message...")

if user_input:
    #show user message
    with st.chat_message("user"):
        st.write(user_input)
    
    #save message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    #geting AI response
    try:
        response = model.generate_content(user_input)
        ai_response = response.text
    except:
        ai_response = "Sorry, error getting response"
    
    #show AI message
    with st.chat_message("assistant"):
        st.write(ai_response)
    
    #save AI response
    st.session_state.messages.append({"role": "assistant", "content": ai_response})