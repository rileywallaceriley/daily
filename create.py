import streamlit as st
import requests
import urllib.parse
import openai

# Display the header image
st.image("https://i.ibb.co/k6cychT/5-C4-FF130-FFD7-4860-B75-F-B442-EB296911.jpg")

# Assuming API keys are stored in Streamlit's secrets
perplexity_api_key = st.secrets["perplexity"]["api_key"]
openai_api_key = st.secrets["openai"]["api_key"]

openai.api_key = openai_api_key

def generate_youtube_search_url(song_title, artist):
    query = f"{song_title} {artist}"
    base_url = "https://www.youtube.com/results?search_query="
    return base_url + urllib.parse.quote(query)

def display_songs_with_links(response_text):
    songs = response_text.strip().split('\n')
    for song in songs:
        if song:
            parts = song.split(' by ')
            if len(parts) == 2:
                title, artist = parts
                youtube_url = generate_youtube_search_url(title, artist)
                st.markdown(f"#### {title} by {artist}")
                st.markdown(f"[Listen on YouTube]({youtube_url})")
            else:
                st.write("Song format not recognized.")

def call_perplexity_api_for_samples(input_text):
    # Function to call Perplexity API for samples
    pass  # Implement the API call as needed

def generate_gpt_playlist_for_vibe(input_text):
    # Function to generate a playlist for a vibe using GPT
    pass  # Implement the API call as needed

# Streamlit UI elements for option selection and input
option = st.selectbox("Choose your option:", ["Sample Train", "Vibe"], index=1)
input_text = st.text_input("Enter a source song or describe your vibe:")

if st.button("Discover Songs"):
    if not input_text:
        st.warning("Please enter the required information.")
    else:
        result = call_api_based_on_option(option, input_text)
        if result:
            st.success('Here are your recommendations:')
            display_songs_with_links(result)
        else:
            st.error("Unable to fetch recommendations. Please try again later or modify your input.")