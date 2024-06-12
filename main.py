# print('hello')

import os
import json

import streamlit as st
import openai

#configuring openai
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))

OPENAI_API_KEY = config_data["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

# print(config_data)

#CONFIGURING STREAMLIT PAGE
st.set_page_config(
    page_title="Nayeer's-GPT",
    page_icon="💬",
    layout="centered"  #or wide
)

#initialize chat session in streamlit if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


#streamlit page title
st.title("🤖 Nayeer's-Gpt-ChatBot")

#display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#input field for users message
user_prompt = st.chat_input("Ask Nayeer's GPT...")

if user_prompt:
    #add user message to chat and display it
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    #send users message to gpt 4 and get a response
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            *st.session_state.chat_history
        ]
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    #display gpt resonse
    with st.chat_message("assistant"):
        st.markdown(assistant_response)