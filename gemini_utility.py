# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 23:10:09 2024

@author: abc
"""

import os
import json
from PIL import Image
import google.generativeai as genai
# get the working directory
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
# load the API key
GOOGLE_API_KEY = config_data['GOOGLE_API_KEY']
# configuring google.generativeai with API key
genai.configure(api_key=GOOGLE_API_KEY)

def load_gemini_pro_model():
    gemini_pro_model = genai.GenerativeModel("gemini-pro")
    return gemini_pro_model

# function fornimage captioning
def gemini_pro_vision_response(prompt, image):
    gemini_pro_vision_model = genai.GenerativeModel("gemini-1.5-flash")
    response = gemini_pro_vision_model.generate_content([prompt, image])
    result = response.text
    return result

# function to get embeddings for text
def embedding_model_response(input_text):
    embedding_model = "models/text-embedding-004"
    embedding = genai.embed_content(model=embedding_model,
                                    content=input_text,
                                    task_type="retrieval_document")
    embedding_list = embedding['embedding']
    return embedding_list

# function to get a response from gemini-pro LLM
def gemini_pro_response(user_prompt):
    gemini_pro_model = genai.GenerativeModel("gemini-pro")
    response = gemini_pro_model.generate_content(user_prompt)
    result = response.text
    return result
