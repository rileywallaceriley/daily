import streamlit as st
import openai
import random
import urllib.parse

# Assuming your OpenAI API key is stored securely in Streamlit's secrets
openai.api_key = st.secrets["openai"]["api_key"]

def setup_page_layout():
    """Displays a randomly selected header image and a welcoming message."""
    st.image(get_random_image())
    # Updated welcoming message with HTML for centering and line spacing
    st.markdown("""
                <style>
                .welcome-message {
                    text-align: center;
                    line-height: 1.5;
                }
                </style>
                <div class="welcome-message">
                    <strong>Welcome to Vibe Cat; share your vibe, and let's find some tunes together.</strong><br><br>
                    Need to switch tabs? No worry, I'll keep your playlist safe here for you. Any errors? Just reload. Meow.<br><br>
                </div>
                """, unsafe_allow_html=True)

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

def generate_intro(vibe):
    """Generates a dynamic introduction based on the selected vibe."""
    intros = [
        f"Crafting a playlist to match the '{vibe}' vibe. Sit back, relax, and enjoy the rhythm. Meow.",
        f"Diving deep into the essence of '{vibe}'. Your tailored tunes are coming up. Meow.",
        f"Exploring the '{vibe}' vibe with some curated beats. Get ready for an auditory adventure. Meow.",
        f"Matching the '{vibe}' mood with some sonic gems. Your journey through music begins now. Meow."
    ]
    return random.choice(intros)

def display_playlist(playlist_content, vibe):
    """Displays the generated playlist content, each song with a YouTube link, and a dynamic introduction."""
    # Add a dynamically generated intro
    st.markdown(generate_intro(vibe), unsafe_allow_html=True)
     # Split the playlist content by new lines and limit to 10 songs
    songs = playlist_content.split('\n')[:10]  # This slices the list to contain only the first 10 elements
    for song in songs:
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
            model="gpt-4-0125-preview", 
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

if st.button("Curate Playlist"):
    if not vibe:
        st.warning("Please enter a vibe to get started.")
    else:
        with st.spinner('Curating your playlist...'):
            playlist_content = generate_playlist(vibe)
            # Make sure the rest of the code inside this block is properly indented as well.
            # Add space before displaying the playlist
            st.write("")
            display_playlist(playlist_content, vibe)

# Add a line and link to Instagram at the bottom of the page
st.markdown("---")
st.markdown(
    """<a href="http://www.instagram.com/rileywallace" target="_blank">Meet my cat dad</a>""", unsafe_allow_html=True)