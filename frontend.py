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
from search_vector_store import search_recipes



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

# HELPER FUNCTIONS

def save_to_file(filename, content):
    with open(filename, 'a') as f:  # 'a' mode to append content
        f.write(content + "\n")  # Add a newline after each entry for better readability

def update_pantry_from_fridge_picture(ingredients, pantryPictue):
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
                                {"type": "text", "text": "can you divde this image intop 20 smaller images and tell me whats in the fridge.  Only return a list of what the fridge contains:"},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                                },
                            ],
                        }
                    ]
        )
        save_to_file('pantry.txt', response.choices[0].message.content)
        
    return response.choices[0].message.content


def read_file(filename):
    with open(filename, 'r') as f:  # 'r' mode to read the file
        content = f.read()  # Read the entire content of the file
    return content


def generate_recipe():
    prompt = f"I have {read_file('pantry.txt')}, What can I cook?,"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=150,
        messages=[
            {"role": "system", "content": "You are a helpful chief."},
            {
                "role": "user",
                "content": prompt,
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
            update = update_pantry_from_fridge_picture(ingredients, image)
            recipe = generate_recipe()
            st.subheader("Here’s what you can cook according to ChatGPT:")
            st.write(recipe)

            recipe_from_vector = search_recipes(ingredients)
            st.subheader("Here’s what you can cook, according to the vector store:")
            st.write(recipe_from_vector)
    else:
        st.warning("Please enter some ingredients first!")