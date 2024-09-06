# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 22:58:31 2024

@author: abc
"""
from streamlit_option_menu import option_menu
import streamlit as st
import os
from gemini_utility import (load_gemini_pro_model,
                            gemini_pro_vision_response,
                            embedding_model_response,
                            gemini_pro_response)
from PIL import Image
working_dir = os.path.dirname(os.path.abspath(__file__))
# setting up page configuration
st.set_page_config(
   page_title="Gemini Pro",
   layout="centered")
#config_data = 
with st.sidebar:
    selected = option_menu("Gemini AI",
                           ["ChatBot",
                            "Image Captioning",
                            "Embed Text",
                            "Ask me anything"],
                            menu_icon = 'robot', 
                            icons=['chat-dots-fill',
                                   'image-fill',
                                   'textarea-t',
                                   'patch-question-fill'],
                           default_index=0)
# function to translate role between gemini pro and streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role =='model':
        return "assistant"
    else:
        return user_role
if selected == 'ChatBot':
    model = load_gemini_pro_model()
    # initialize chat session in streamlit
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])
        
    # streamlit page title
    st.title("ChatBot")
    # display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)
    # input field for user's message
    user_prompt = st.chat_input("Ask Gemini Pro...")
    if user_prompt:
        st.chat_message("user").markdown(user_prompt)
        gemini_response = st.session_state.chat_session.send_message(user_prompt)
        # display gemini pro response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)
# Image captioning page
if selected == "Image Captioning":
    # streamlit page title
    st.title("Image Narration")
    uploaded_image = st.file_uploader("Upload an Image...",type=["jpg","png","jpeg"])
    if st.button("Generate Caption"):
        image = Image.open(uploaded_image)
        col1,col2 = st.columns(2)
        with col1:
            resized_image = image.resize((800,800))
            st.image(resized_image)
        default_prompt="Write a caption for this image to understand what's in it"
        # getting the response from gemini flash
        caption = gemini_pro_vision_response(default_prompt, image)
        with col2:
            st.info(caption)
# Text Embedding Page
if selected == "Embed Text":
    st.title("Embed Text")
    # input text box
    input_text =  st.text_area(label="",placeholder="Enter the text to get the embeddings")
    if st.button("Get Embeddings"):
        response = embedding_model_response(input_text)
        st.markdown(response)
# Question Answering Page
if selected == "Ask me anything":
    st.title("Ask me a question")
    # text box to enter prompt
    user_prompt = st.text_area(label="",placeholder="Ask Gemini Pro...")
    if st.button("Get response"):
        response = gemini_pro_response(user_prompt)
        st.markdown(response)