import streamlit as st
import openai
import random
import urllib.parse

# Assuming your OpenAI API key is stored securely in Streamlit's secrets
openai.api_key = st.secrets["openai"]["api_key"]

def setup_page_layout():
    """Displays a randomly selected header image and a welcoming message."""
    st.image(get_random_image())
    st.write("Welcome to Vibe Cat; share your vibe, and let's find some tunes together. Need to switch tabs? No worry, I'll keep your playlist safe here so you can visit it throughout the day. Any errors? Just reload. Meow.")
    st.write("Meet my Cat Dad: instagram.com/rileywallace")

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

def display_playlist(playlist_content):
    """Displays the generated playlist content, each song with a YouTube link."""
    songs = playlist_content.split('\n')
    for song in songs:
        # Clean song info to remove numbers and asterisks
        song_info_clean = song.lstrip('0123456789.* ')
        if ' by ' in song_info_clean:
            parts = song_info_clean.split(' by ')
            if len(parts) == 2:
                song_title, main_artist = parts
                youtube_url = generate_youtube_search_url(song_title.strip(), main_artist.strip())
                st.markdown(f"**{song_title.strip()}** by {main_artist.strip()} [Listen on YouTube]({youtube_url})", unsafe_allow_html=True)

def generate_playlist(vibe):
    """Generates a playlist based on the given vibe using the GPT-4 Chat model."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-0125-preview",  # Use the Chat model
            messages=[
                {"role": "system", "content": "You are a knowledgeable music enthusiast. Generate a playlist based on a given vibe, listing songs in 'song_title by artist' format."},
                {"role": "user", "content": f"Vibe: {vibe}"}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return ""

setup_page_layout()

vibe = st.text_input("What's your vibe?")
include_top_40 = st.checkbox("Include Top 40")
stay_super_random = st.checkbox("Stay Super Random")

if 'playlist_content' not in st.session_state or vibe != st.session_state.get('last_vibe', ''):
    if st.button("Curate Playlist"):
        if not vibe:
            st.warning("Please enter a vibe to get started.")
        else:
            with st.spinner('Curating your playlist...'):
                playlist_content = generate_playlist(vibe)
                # Store the generated playlist and the current vibe in the session state.
                st.session_state['playlist_content'] = playlist_content
                st.session_state['last_vibe'] = vibe
                display_playlist(playlist_content)
else:
    # Display the stored playlist without regenerating it.
    display_playlist(st.session_state['playlist_content'])
