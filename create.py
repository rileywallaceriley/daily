import streamlit as st
import openai
import random
import urllib.parse

# Configure your OpenAI API key here or fetch it from Streamlit's secrets
openai.api_key = st.secrets["openai"]["api_key"]

def setup_page_layout():
    """Sets up the page layout, including a header image."""
    st.image(get_random_image())
    st.write("Welcome to Vibe Cat! Share your vibe, and let's discover some tunes.")

def get_random_image():
    """Returns a random image URL."""
    image_urls = [
        "https://i.ibb.co/BNHvHM0/684518-B3-B7-D0-45-D7-8801-2355-D70-D169-C.webp",
        "https://i.ibb.co/LJQZ9s7/33540-C0-B-E7-DE-48-CC-AA39-64-BA2-E57-B264.jpg",
        "https://i.ibb.co/gZ0wVhR/24-E8737-A-108-A-4-FB6-81-A8-34566-DA12-CCA.jpg",
        "https://i.ibb.co/k6cychT/5-C4-FF130-FFD7-4860-B75-F-B442-EB296911.jpg"
    ]
    return random.choice(image_urls)

def display_playlist(playlist_content):
    """Displays the generated playlist and provides a copy to clipboard feature."""
    st.text(playlist_content)
    
    # Button to copy the playlist to the clipboard
    if st.button('Copy Playlist'):
        st.markdown(f'''
            <textarea readonly id="txt_area" style="height: 0;width: 0;opacity: 0;">{playlist_content}</textarea>
            <button onclick="navigator.clipboard.writeText(document.getElementById('txt_area').value)">Copy to Clipboard</button>
            ''', unsafe_allow_html=True)
        st.success('Playlist copied to clipboard!')

def generate_playlist(vibe):
    """Generates a playlist based on the vibe using GPT-4 and returns it as a string."""
    response = openai.ChatCompletion.create(
        model="gpt-4-0125-preview",
        messages=[
            {"role": "system", "content": "Generate a playlist based on the given vibe."},
            {"role": "user", "content": vibe}
        ]
    )
    return response.choices[0].message['content']

# UI Setup
setup_page_layout()
vibe_input = st.text_input("What's your vibe?")

if st.button("Generate Playlist"):
    if vibe_input:
        with st.spinner('Generating your playlist...'):
            playlist = generate_playlist(vibe_input)
        display_playlist(playlist)
    else:
        st.warning("Please enter a vibe to get started.")