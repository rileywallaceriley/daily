import os
import requests
import streamlit as st

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('PERPLEXITY_API_KEY')

if api_key is None:
    st.error("Perplexity API key not found. Please set the PERPLEXITY_API_KEY environment variable.")
else:
    # Streamlit app interface
    st.title('Sample Explorer')

    # User inputs for song and artist
    song = st.text_input('Enter the song title:')
    artist = st.text_input('Enter the artist name:')

    if st.button('Find Samples'):
        if song and artist:
            # Formulating the query for real-time data
            query = f"Provide real-time information on the samples used in '{song}' by {artist}."

            # Setting up the API request
            url = 'https://api.perplexity.ai/chat/completions'
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            payload = {
                "model": "sonar-medium-online",  # Specify the model capable of real-time searches
                "messages": [
                    {
                        "role": "user",
                        "content": query
                    }
                ]
            }

            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                insights = response.json()['choices'][0]['message']['content']
                st.write(insights)
            else:
                st.error(f"Failed with status code {response.status_code}: {response.text}")
        else:
            st.warning('Please enter both a song title and an artist name to find samples.')