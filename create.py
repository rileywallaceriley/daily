import streamlit as st
import openai
import random
import urllib.parse

def setup_page_layout():
    """Sets up the page layout with a fixed intro and displays a randomly selected image."""
    st.image(get_random_image())
    st.write("Welcome to Vibe Cat; give me your vibe (a song you love, a feeling, etc.), and I'll curate a great playlist for you.")

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

def generate_youtube_search_url(song_title, main_artist):
    """Generates a YouTube search URL for a given song title and main artist."""
    query = f"{song_title} {main_artist}".replace(" ", "+")
    base_url = "https://www.youtube.com/results?search_query="
    return base_url + urllib.parse.quote_plus(query)

def display_song_with_link(song_title, main_artist):
    """Displays a song title and main artist with a link to search the song on YouTube."""
    youtube_url = generate_youtube_search_url(song_title, main_artist)
    st.markdown(f"**{song_title}** by {main_artist} [Listen on YouTube]({youtube_url})", unsafe_allow_html=True)

def generate_playlist_intro_and_songs(vibe, include_top_40, stay_super_random):
    """Generates an introduction and a playlist based on the user's vibe using OpenAI's GPT-4."""
    prompt = f"Describe the vibe '{vibe}', then generate a playlist based on it. Include an introduction about the vibe and list songs formatted as 'song_title by main_artist'."
    
    response = openai.ChatCompletion.create(
        model="gpt-4-0125-preview",  # Correct GPT model
        prompt=prompt,
        temperature=0.7,
        max_tokens=1024,
        n=1,
        stop=None,
        api_key=st.secrets["openai"]["api_key"]
    )
    return response.choices[0].text.strip()

# Display the header image and introductory text
setup_page_layout()

# User inputs for vibe, preferences, and button to generate playlist
input_text = st.text_input("Enter your vibe:")
include_top_40 = st.checkbox("Include Top 40")
stay_super_random = st.checkbox("Stay Super Random")

if st.button("Curate Playlist"):
    if not input_text:
        st.warning("Please enter the required information.")
    else:
        with st.spinner('Curating your playlist...'):
            playlist_content = generate_playlist_intro_and_songs(input_text, include_top_40, stay_super_random)
            intro, *songs = playlist_content.split('\n')
            st.write(intro)  # Display the intro
            for song in songs:
                if ' by ' in song:
                    song_title, main_artist = song.split(' by ')
                    display_song_with_link(song_title.strip(), main_artist.strip())