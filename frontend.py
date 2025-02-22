import streamlit as st
import pandas as pd
import numpy as np
import openai
import os
from os import environ
from dotenv import load_dotenv
from PIL import Image
from google.cloud import vision
import io
import base64


# OPEN AI SETUP
load_dotenv()

OPENAI_API_KEY = environ["OPENAI_API_KEY"]


client = openai.OpenAI(api_key=OPENAI_API_KEY)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

base64_image = encode_image("pictures/idk.jpg")

# IMAGE SETUP

uploaded_file = st.file_uploader("Upload an image to save...", type=["jpg", "jpeg", "png"])

# AN IDIOT TRYNA FIGURE IT OUT 

def get_recipe(ingredients, pantryPictue):
    prompt = f"I have {ingredients}. What can I cook?"

    if pantryPictue is not None:

        prompt = f"I have {ingredients}, plus anything you see in this picture of my fridge, What can I cook?,"
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            # messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "can you divde this image intop 20 smaller images and tell me whats in the fridge"},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                                },
                            ],
                        }
                    ]
        )
        
    return response.choices[0].message.content


st.title('Recipe Recommender')
st.write("Enter your ingredients and get recipe suggestions!")
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption=f'Uploaded {uploaded_file.name}', use_column_width=True)

# User input
ingredients = st.text_input("Enter ingredients (comma-separated):", "")

# print recipe on the UI
if st.button("Generate Recipe"):
    if ingredients:
        with st.spinner("Generating recipe..."):
            recipe = get_recipe(ingredients, image)
            st.subheader("Here’s what you can cook:")
            st.write(recipe)
    else:
        st.warning("Please enter some ingredients first!")