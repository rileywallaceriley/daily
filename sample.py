import os
import requests
import streamlit as st
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve API keys from Streamlit secrets for deployment or from environment variables for local development
PERPLEXITY_API_KEY = st.secrets["perplexity"]["api_key"] if 'perplexity' in st.secrets else os.getenv('PERPLEXITY_API_KEY')
OPENAI_API_KEY = st.secrets["openai"]["api_key"] if 'openai' in st.secrets else os.getenv('OPENAI_API_KEY')

def fetch_song_samples(song, artist):
    """Fetches song samples details from the Perplexity API."""
    url = 'https://api.perplexity.ai/v1/chat/completions'  # Ensure this is the correct endpoint for your use
    headers = {
        'Authorization': f'Bearer {PERPLEXITY_API_KEY}',
        'Content-Type': 'application/json',
    }
    payload = {
        "model": "sonar-medium-online",  # or your specific model
        "messages": [
            {"role": "user", "content": f"Provide real-time information on the samples used in '{song}' by {artist}."}
        ]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"Perplexity API call failed with status {response.status_code}: {response.text}")

def format_response_with_gpt4(details):
    """Formats the response using GPT-4 chat model."""
    openai.api_key = OPENAI_API_KEY
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": "You are a knowledgeable music enthusiast. Help format this information and generate a YouTube search link."},
                {"role": "user", "content": details}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        raise Exception(f"Error with OpenAI: {str(e)}")

# Streamlit app interface
st.title('Sample Explorer')

# User inputs
song = st.text_input('Enter the song title:')
artist = st.text_input('Enter the artist name:')

if st.button('Find Samples'):
    if song and artist:
        try:
            samples_details = fetch_song_samples(song, artist)
            formatted_response = format_response_with_gpt4(samples_details)
            st.markdown(formatted_response)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning('Please enter both a song title and an artist name to find samples.')