import openai
import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

# Connect to the index

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index_name = "recipe-indexjv"
index = pc.Index(index_name)

def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def search_recipes(user_input):
    query_vector = get_embedding(user_input)
    
    results = index.query(
        vector=query_vector,
        top_k=3,  # Get top 3 similar recipes
        include_metadata=True
    )
    
    my_list = []
    for match in results["matches"]:
        my_list.append(f"Recipe: {match['metadata']['text']}, Score: {match['score']}")
    return my_list