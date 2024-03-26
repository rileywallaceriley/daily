import streamlit as st
import requests
import urllib.parse
import openai

# Assuming API keys are stored in Streamlit's secrets
perplexity_api_key = st.secrets["perplexity"]["api_key"]
openai_api_key = st.secrets["openai"]["api_key"]

openai.api_key = openai_api_key

def generate_youtube_search_url(query):
    base_url = "https://www.youtube.com/results?search_query="
    query = urllib.parse.quote(query)
    return base_url + query

def process_and_display_songs(response_text):
    """
    Processes the AI's text response to extract song details and display them with YouTube URLs.
    Adjust this logic based on the actual format of your AI's response.
    """
    songs = response_text.split('\n')  # Assuming each song detail is on a new line
    for song in songs:
        if song.strip():  # Ensure it's not an empty line
            # Directly use the song string as the search query
            youtube_url = generate_youtube_search_url(song)
            st.markdown(f"- {song} [Listen on YouTube]({youtube_url})", unsafe_allow_html=True)

def call_perplexity_api(input_text):
    # Your existing Perplexity API call logic

def generate_gpt_playlist(vibe):
    # Your existing GPT playlist generation logic

# Streamlit UI setup
option = st.selectbox("Choose your option:", ["Sample Train", "Vibe"], index=1)
input_text = st.text_input("Enter a source song or describe your vibe:")

if st.button("Vibes"):
    if not input_text:
        st.warning("Please enter the required information.")
    else:
        with st.spinner('Fetching songs...'):
            if option == "Sample Train":
                result = call_perplexity_api(input_text)
            else:  # Vibe
                result = generate_gpt_playlist(input_text)
                
            if result:
                st.success('Here are your vibes 😎:')
                process_and_display_songs(result)
            else:
                st.error("Unable to fetch recommendations. Please try again later or modify your input.")