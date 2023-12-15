import streamlit as st
import time
from functions import *


appInfo()

st.title("My Assistant")

with st.chat_message("assistant"):
    st.write("Hello 👋")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    
    try:
        response = assistant(prompt)
    except:
        st.error('Assistant failed!')
        st.stop()

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = response

        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response:
            full_response += chunk + " "
            time.sleep(0.01)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(assistant_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

