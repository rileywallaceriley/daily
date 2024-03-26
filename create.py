import streamlit as st
import requests
import urllib.parse
import openai

# Display the header image
st.image("https://i.ibb.co/k6cychT/5-C4-FF130-FFD7-4860-B75-F-B442-EB296911.jpg")

# Assuming API keys are stored in Streamlit's secrets
perplexity_api_key = st.secrets["perplexity"]["api_key"]
openai_api_key = st.secrets["openai"]["api_key"]

# Set the OpenAI API key for usage in calls
openai.api_key = openai_api_key

def generate_youtube_search_url(song_title, artist=""):
    """Generates a YouTube search URL."""
    query = f"{song_title} {artist}".strip()
    base_url = "https://www.youtube.com/results?search_query="
    return base_url + urllib.parse.quote(query)

def display_song_with_link(song_detail):
    """Displays enumerated song details with a YouTube link."""
    # Remove enumeration and split on "-" to separate song title from artist(s)
    song_info = song_detail.split('. ', 1)[-1].split(' - ', 1)
    if len(song_info) == 2:
        song_title, artist_info = song_info
        youtube_url = generate_youtube_search_url(song_title, artist_info.split(' feat.')[0])  # Removes featured artists for the search
        st.markdown(f"**{song_title}** by {artist_info} [Listen on YouTube]({youtube_url})", unsafe_allow_html=True)
    else:
        st.write(f"Unable to parse song detail: {song_detail}")

def generate_gpt_playlist_for_vibe(vibe):
    """Generates a playlist for a vibe."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": "Generate a playlist for the given vibe, including song titles and artists."},
                {"role": "user", "content": vibe}
            ]
        )
        playlist_response = response.choices[0].message['content'].strip()
        return playlist_response
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# UI setup for option selection and input
option = st.selectbox("Choose your option:", ["Sample Train", "Vibe"], index=1)
input_text = st.text_input("Enter a source song or describe your vibe:")

if st.button("Discover Songs"):
    if not input_text:
        st.warning("Please enter the required information.")
    else:
        result = None
        if option == "Vibe":
            with st.spinner('Generating a vibe playlist...'):
                result = generate_gpt_playlist_for_vibe(input_text)

        if result:
            st.success('Here are your recommendations:')
            for line in result.split('\n'):
                display_song_with_link(line)
        else:
            st.error("Unable to fetch recommendations. Please try again later or modify your input.")