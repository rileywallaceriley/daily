import os
import requests
import streamlit as st
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv('PERPLEXITY_API_KEY')

# List of image URLs
images = [
    "https://i.ibb.co/619XbBp/6-E8-A603-C-C1-C3-4362-A7-F6-1454727-A0-FA2.webp",
    "https://i.ibb.co/Fb2tYMn/BF6-D9953-9110-49-E5-BBF2-58502-B5-D45-AC.webp",
    "https://i.ibb.co/tPbXKhw/D7-B37254-223-A-43-B7-9-AAA-8-A7-F7-E011040.jpg",
    "https://i.ibb.co/gTjrdqb/BC7949-E4-9729-45-EA-9-CB4-E820-C3686-D94.webp"
]

# Randomly choose an image
chosen_image = random.choice(images)

# Display the chosen image
st.image(chosen_image, use_column_width=True)

# Update the header with the new copy using regular font weight
st.markdown("Hi, I’m Vibe Pup; give me any song and I’ll sniff out the samples used to make it, woof.")

if api_key is None:
    st.error("Perplexity API key not found. Please set the PERPLEXITY_API_KEY environment variable.")
else:
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
            # Add a line and link to Instagram at the bottom of the page
st.markdown("---")
st.markdown(
    """<a href="http://www.instagram.com/rileywallace" target="_blank">Meet my cat dad</a>""", unsafe_allow_html=True)