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

def display_song_with_link(line):
    """Displays song details with a YouTube link, skips non-song lines."""
    non_song_keywords = ["playlist", "vibe", "incorporates", "listeners", "tracks", "selection"]
    if any(keyword in line.lower() for keyword in non_song_keywords):
        # This line is likely part of the intro or outro, display as regular text.
        st.write(line)
    else:
        # This line is likely a song title, process and display with YouTube link.
        song_info = line.split(' by ')
        if len(song_info) >= 2:
            song_title, artist_info = song_info[0], ' by '.join(song_info[1:])
            youtube_url = generate_youtube_search_url(song_title, artist_info.split(' ft.')[0].split(',')[0])  # Simplify artist info for search
            st.markdown(f"**{song_title}** by {artist_info} [Listen on YouTube]({youtube_url})", unsafe_allow_html=True)
        else:
            st.error(f"Unable to parse song detail: {line}")

# UI setup for option selection and input
input_text = st.text_input("Enter a vibe:")

if st.button("Generate Playlist"):
    if not input_text:
        st.warning("Please enter a vibe to generate a playlist.")
    else:
        # Placeholder for GPT call to generate a playlist
        # Replace with actual function to fetch playlist from GPT-4
        playlist = """Your GPT-4 playlist generation logic here, 
                      returning a string that includes the playlist details."""
        
        if playlist:
            st.success('Playlist Generated:')
            for line in playlist.split('\n'):
                if line.strip():  # Check if line is not empty
                    display_song_with_link(line.strip())
        else:
            st.error("Unable to fetch recommendations. Please try again.")