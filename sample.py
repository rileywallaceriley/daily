import os
import requests
import streamlit as st
import openai

# Load environment variables if running locally, for Streamlit Cloud use st.secrets
PERPLEXITY_API_KEY = st.secrets["perplexity"]["api_key"]
OPENAI_API_KEY = st.secrets["openai"]["api_key"]

def fetch_song_samples(song, artist):
    """Fetches song samples details from Perplexity."""
    url = 'https://api.perplexity.ai/chat/completions'
    headers = {
        'Authorization': f'Bearer {PERPLEXITY_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        "model": "sonar-medium-online",
        "messages": [
            {"role": "user", "content": f"Provide real-time information on the samples used in '{song}' by {artist}."}
        ]
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"Perplexity API call failed with status {response.status_code}")

def format_response_with_gpt4(song_details):
    """Formats song details using GPT-4."""
    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(
        model="gpt-4-0125-preview",
        prompt=f"Format the following song details into a concise summary: {song_details}\n\nGenerate a YouTube search link based on the song details.",
        temperature=0.7,
        max_tokens=150
    )
    return response.choices[0].text

st.title('Sample Explorer')

song = st.text_input('Song title:')
artist = st.text_input('Artist name:')

if st.button('Find Samples'):
    if song and artist:
        try:
            samples_details = fetch_song_samples(song, artist)
            formatted_response = format_response_with_gpt4(samples_details)
            st.markdown(formatted_response)
        except Exception as e