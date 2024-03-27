import streamlit as st
import openai
import random
import urllib.parse

# Function to set up the page layout and display a random image
def setup_page_layout():
    """Sets up the page layout with a fixed intro and displays a randomly selected image."""
    st.image(get_random_image())
    st.write("Welcome to Vibe Cat; give me your vibe (a song you love, a feeling, etc.), and I'll curate a great playlist for you.")

# Function to select a random image only once per session
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

# Function to generate a YouTube search URL
def generate_youtube_search_url(song_title, main_artist):
    """Generates a YouTube search URL for a given song title and main artist."""
    query = f"{song_title}+{main_artist}".replace(" ", "+")
    base_url = "https://www.youtube.com/results?search_query="
    return base_url + urllib.parse.quote_plus(query)

# Function to display each song with a YouTube link
def display_playlist(playlist_content):
    """Displays the playlist, filtering out non-song lines and showing song links."""
    lines = playlist_content.split('\n')
    for line in lines:
        if line.strip() and line.lstrip('0123456789.- ').startswith('"') and '-' in line:
            try:
                parts = line.strip().split('"')[1].split(' - ')
                song_title = parts[0].strip()
                artist_name = parts[1].split(' ft.')[0].split(' feat.')[0].split(',')[0].strip()
                youtube_url = generate_youtube_search_url(song_title, artist_name)
                st.markdown(f"**{song_title}** by {artist_name} [Listen on YouTube]({youtube_url})", unsafe_allow_html=True)
            except IndexError:
                st.error(f"Could not process line for YouTube link: {line}")
        elif line.strip() and not line.lstrip('0123456789.- ').startswith('"'):
            st.write(line)  # Display contextual text

# Function to generate a playlist based on user's vibe using GPT-4
def generate_gpt_playlist_intro_and_songs(vibe, include_top_40, stay_super_random):
    """Generates an introduction and a playlist based on the user's vibe using GPT-4."""
    prompt = f"Describe the vibe '{vibe}', then generate a playlist based on it. " \
             "Start with an introduction about the vibe, followed by song titles and main artists. " \
             "Exclude additional commentary for each song."
    if include_top_40:
        prompt += " Include popular songs mixed with unknown ones."
    if stay_super_random:
        prompt += " Focus on b-sides, under-hailed gems, and otherwise underground music."
    response = openai.ChatCompletion.create(
        model="gpt-4-0125-preview",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": "Please describe the vibe and generate the playlist."}
        ]
    )
    return response.choices[0].message['content'].strip()

# Main app setup and interaction
setup_page_layout()
openai_api_key = st.secrets["openai"]["api_key"]
openai.api_key = openai_api_key

input_text = st.text_input("Enter your vibe:")
include_top_40 = st.checkbox("Include Top 40")
stay_super_random = st.checkbox("Stay Super Random")

if st.button("Curate Playlist"):
    if not input_text:
        st.warning("Please  enter the required information.")
    else:
        with st.spinner('Curating your playlist...'):
            playlist_content = generate_gpt_playlist_intro_and_songs(input_text, include_top_40, stay_super_random)
            display_playlist(playlist_content)