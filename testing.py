from flask import Flask
from flask import jsonify, request 
from os import environ
from openai import OpenAI
from dotenv import load_dotenv
from flask_cors import CORS 
# app = Flask(__name__)
# CORS(app)


load_dotenv()

OPENAI_API_KEY = environ["OPENAI_API_KEY"]

client = OpenAI()

# @app.route('/findfood', methods=['POST'])
def get_output():
    lol = f"wheat, barley, water and time. with these 4 ingridents what can i make "
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=150,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": lol,
            }
        ],
    )
    # restaurant_names = extract_restaurant_names(response.choices[0].message.content)
    # data = []
    # for name in restaurant_names:
    #     params = {"location": location, "name": name}
    #     data.append(yelp_api_client.get_data_from_yelp(params=params)["businesses"][0])
    #     # appends yelp data
    # lol = {
    #     "data": data
    # }
    # return jsonify(lol)
    print(response.choices[0].message.content)



get_output()
# if __name__ == '__main__':
#     app.run(debug=True)
