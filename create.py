import re
import streamlit as st
import urllib.parse
import openai

# Display the header image
st.image("https://i.ibb.co/k6cychT/5-C4-FF130-FFD7-4860-B75-F-B442-EB296911.jpg")

# Assuming API keys are stored in Streamlit's secrets
openai_api_key = st.secrets["openai"]["api_key"]

# Set the OpenAI API key for usage in calls
openai.api_key = openai_api_key

def generate_youtube_search_url(song_title, artist=""):
    """Generates a YouTube search URL."""
    query = f"{song_title} {artist}".strip()
    base_url = "https://www.youtube.com/results?search_query="
    return base_url + urllib.parse.quote(query)

def display_song_with_link(song_detail):
    """Displays song details with a YouTube link or regular text for non-song lines."""
    # Attempt to identify song lines based on expected pattern
    if " - " in song_detail:
        song_info = re.sub(r'^\d+\.\s*', '', song_detail).split(' - ', 1)
        if len(song_info) == 2:
            song_title, artist_info = song_info
            youtube_url = generate_youtube_search_url(song_title, artist_info.split(' feat.')[0])  # Removes featured artists for search
            st.markdown(f"**{song_title}** by {artist_info} [Listen on YouTube]({youtube_url})", unsafe_allow_html=True)
        else:
            st.error(f"Unable to parse song detail: {song_detail}")
    else:
        # Display as regular text for intro/outro or non-song lines
        st.write(song_detail)

# UI setup for option selection and input (Placeholder for actual GPT call implementation)
input_text = st.text_input("Enter a vibe:")

if st.button("Generate Playlist"):
    if not input_text:
        st.warning("Please enter a vibe to generate a playlist.")
    else:
        playlist = "Your function to fetch playlist from GPT-4"  # Placeholder for actual GPT call
        if playlist:
            st.success('Playlist Generated:')
            for line in playlist.split('\n'):
                display_song_with_link(line.strip())
        else:
            st.error("Unable to fetch recommendations. Please try again.")