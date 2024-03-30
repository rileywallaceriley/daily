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

st.markdown("Hi, I’m Vibe Pup; give me any song or album and I’ll sniff out the samples used to make it, woof.")

if api_key is None:
    st.error("Perplexity API key not found. Please set the PERPLEXITY_API_KEY environment variable.")
else:
    # Dropdown to select search by song or album
    search_type = st.selectbox('Search by:', ['Song', 'Album'])

    # User inputs for song or album, and artist name
    song_or_album = st.text_input(f'Enter the {search_type.lower()} title:')
    artist_name = st.text_input('Enter the artist name:')
    
    # Checkbox for reverse search
    reverse_search = st.checkbox('Reverse?')

    if st.button('Find Samples'):
        if song_or_album and artist_name:
            # Adjusting the query based on the user's choices
            query_context = "notable songs that sampled this" if reverse_search else "samples used to make this"
            query = f"Provide real-time information on {query_context} '{song_or_album}' by '{artist_name}'."

            # API request setup remains the same
            url = 'https://api.perplexity.ai/chat/completions'
            headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json', 'Accept': 'application/json'}
            payload = {"model": "sonar-medium-online", "messages": [{"role": "user", "content": query}]}

            # Display a loading message while fetching data
            with st.spinner(f"Fetching {query_context} for '{song_or_album}' by '{artist_name}'..."):
                response = requests.post(url, headers=headers, json=payload)

                if response.status_code == 200:
                    insights = response.json()['choices'][0]['message']['content']
                    st.write(insights)
                else:
                    st.error(f"Failed with status code {response.status_code}: {response.text}")
        else:
            st.warning('Please enter both the title and artist name to find samples.')