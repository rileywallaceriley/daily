import os
import requests
import streamlit as st
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv('PERPLEXITY_API_KEY')

# Display a random "Vibe Pup" image
images = [
    "https://i.ibb.co/619XbBp/6-E8-A603-C-C1-C3-4362-A7-F6-1454727-A0-FA2.webp",
    "https://i.ibb.co/Fb2tYMn/BF6-D9953-9110-49-E5-BBF2-58502-B5-D45-AC.webp",
    "https://i.ibb.co/tPbXKhw/D7-B37254-223-A-43-B7-9-AAA-8-A7-F7-E011040.jpg",
    "https://i.ibb.co/gTjrdqb/BC7949-E4-9729-45-EA-9-CB4-E820-C3686-D94.webp"
]
chosen_image = random.choice(images)
st.image(chosen_image, use_column_width=True)

st.markdown("Hi, I’m Vibe Pup; give me any song and I’ll sniff out the samples used to make it, woof.")

if api_key is None:
    st.error("Perplexity API key not found. Please set the PERPLEXITY_API_KEY environment variable.")
else:
    song_title = st.text_input('Enter the song title:')
    artist_name = st.text_input('Enter the artist name:')
    reverse_search = st.checkbox('Reverse?')

    if st.button('Find Samples'):
        if song_title and artist_name:
            # Change the query based on the checkbox
            if reverse_search:
                query = f"Provide real-time information on songs that sample '{song_title}' by '{artist_name}'."
            else:
                query = f"Provide real-time information on the samples used in the song '{song_title}' by '{artist_name}'."

            # API request setup
            url = 'https://api.perplexity.ai/chat/completions'
            headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json', 'Accept': 'application/json'}
            payload = {"model": "sonar-medium-online", "messages": [{"role": "user", "content": query}]}

            with st.spinner('Fetching...'):
                response = requests.post(url, headers=headers, json=payload)

                if response.status_code == 200:
                    insights = response.json()['choices'][0]['message']['content']
                    st.write(insights)
                else:
                    st.error(f"Failed with status code {response.status_code}: {response.text}")
        else:
            st.warning('Please enter both the song title and artist name to find samples.')