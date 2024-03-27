import streamlit as st
import openai
import random
import urllib.parse

# Assuming your OpenAI API key is set in Streamlit's secrets for enhanced security
openai.api_key = st.secrets["openai"]["api_key"]

def setup_page_layout():
    """Displays a randomly selected header image and a welcoming message."""
    st.image(get_random_image())
    st.write("Welcome to Vibe Cat; share your vibe, and let's find some tunes together.")

def get_random_image():
    """Returns a random image URL from a predefined list."""
    image_urls = [
        "https://i.ibb.co/BNHvHM0/684518-B3-B7-D0-45-D7-8801-2355-D70-D169-C.webp",
        "https://i.ibb.co/LJQZ9s7/33540-C0-B-E7-DE-48-CC-AA39-64-BA2-E57-B264.jpg",
        "https://i.ibb.co/gZ0wVhR/24-E8737-A-108-A-4-FB6-81-A8-34566-DA12-CCA.jpg",
        "https://i.ibb.co/k6cychT/5-C4-FF130-FFD7-4860-B75-F-B442-EB296911.jpg"
    ]
    return random.choice(image_urls)

def generate_youtube_search_url(song_title, main_artist):
    """Generates a YouTube search URL for the given song title and artist."""
    query = f"{song_title} {main_artist}".replace(" ", "+")
    base_url = "https://www.youtube.com/results?search_query="
    return base_url + urllib.parse.quote_plus(query)

def generate_playlist(vibe):
    """Generates a playlist based on the given vibe using the GPT-4 model."""
    try:
        response = openai.Completion.create(
            model="gpt-4-0125-preview",  # Explicitly specify GPT-4 model
            prompt=f"Generate a playlist for the vibe: '{vibe}'. List songs in 'song_title by artist' format.",
            temperature=0.7,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response.choices[0].text.strip()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return ""

def display_playlist(playlist_content):
    """Displays the generated playlist content, each song with a YouTube link."""
    songs = playlist_content.split('\n')
    for song in songs:
        if ' by ' in song:
            parts = song.split(' by ')
            if len(parts) == 2:
                song_title, main_artist = parts
                youtube_url = generate_youtube_search_url(song_title.strip(), main_artist.strip())
                st.markdown(f"**{song_title.strip()}** by {main_artist.strip()} [Listen on YouTube]({youtube_url})", unsafe_allow_html=True)

setup_page_layout()

vibe = st.text_input("What's your vibe?")
include_top_40 = st.checkbox("Include Top 40")
stay_super_random = st.checkbox("Stay Super Random")

if st.button("Curate Playlist"):
    if not vibe:
        st.warning("Please enter a vibe to get started.")
    else:
        playlist_content = generate_playlist(vibe)
        display_playlist(playlist_content)