import streamlit as st
import openai
import random
import urllib.parse

def get_random_image():
    """Selects a random image only once per session."""
    if 'image_url' not in st.session_state:
        image_urls = [
            "https://i.ibb.co/BNHvHM0/684518-B3-B7-D0-45-D7-8801-2355-D70-D169-C.webp",
            "https://i.ibb.co/LJQZ9s7/33540-C0-B-E7-DE-48-CC-AA39-64-BA2-E57-B264.jpg",
            "https://i.ibb.co/gZ0wVhR/24-E8737-A-108-A-4-FB6-81-A8-34566-DA12-CCA.jpg",
            "https://i.ibb.co/k6cychT/5-C4-FF130-FFD7-4860-B75-F-B442-EB296911.jpg"
        ]
        st.session_state['image_url'] = random.choice(image_urls)
    return st.session_state['image_url']

# Display the header image using session state
st.image(get_random_image())

# Contextual text under the image
st.write("Welcome to Vibe Cat; give me your vibe (a song you love, a feeling, etc.) and I'll curate a great playlist.")

# API keys stored in Streamlit's secrets for security
openai_api_key = st.secrets["openai"]["api_key"]

# Set the OpenAI API key for usage in calls to GPT-4
openai.api_key = openai_api_key

def generate_youtube_search_url(song_title, artist=""):
    """Generates a YouTube search URL for a given song title and artist."""
    query = f"{song_title} {artist}".strip()
    base_url = "https://www.youtube.com/results?search_query="
    return base_url + urllib.parse.quote_plus(query)

def display_song_with_link(song_title, artist):
    """Displays a song title and artist with a link to search the song on YouTube."""
    youtube_url = generate_youtube_search_url(song_title, artist)
    st.markdown(f"**{song_title} by {artist}** [Listen on YouTube]({youtube_url})", unsafe_allow_html=True)

def generate_gpt_playlist(vibe, include_top_40, stay_super_random):
    """Generates a playlist based on the user's vibe and preferences using GPT-4."""
    prompt = f"Generate a playlist based on the vibe '{vibe}'."
    if include_top_40:
        prompt += " Include popular songs mixed with unknown ones."
    if stay_super_random:
        prompt += " Focus on b-sides, under-hailed gems, and otherwise underground music."
        
    response = openai.ChatCompletion.create(
        model="gpt-4-0125-preview",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": "Please generate the playlist."}
        ]
    )
    playlist_content = response.choices[0].message['content'].strip()
    st.success('Here is your curated playlist:')
    for line in playlist_content.split('\n'):
        if ' - ' in line:
            parts = line.split(' - ')
            if len(parts) >= 2:
                song_title, artist = parts[0].strip(), parts[1].strip()
                display_song_with_link(song_title, artist)
        else:
            st.write(line)  # Handle contextual or descriptive lines

# UI setup for input, checkboxes, and button to generate playlist
input_text = st.text_input("Enter your vibe:")
include_top_40 = st.checkbox("Include Top 40")
stay_super_random = st.checkbox("Stay Super Random")

if st.button("Curate Playlist"):
    if not input_text:
        st.warning("Please enter the required information.")
    else:
        with st.spinner('Curating your playlist...'):
            generate_gpt_playlist(input_text, include_top_40, stay_super_random)
