import streamlit as st
import urllib.parse
import requests
import openai

# Display the header image
st.image("https://i.ibb.co/k6cychT/5-C4-FF130-FFD7-4860-B75-F-B442-EB296911.jpg")

# API keys stored in Streamlit's secrets for security
perplexity_api_key = st.secrets["perplexity"]["api_key"]
openai_api_key = st.secrets["openai"]["api_key"]

# Set the OpenAI API key for usage in calls to GPT-4
openai.api_key = openai_api_key

def generate_youtube_search_url(song_title, artist=""):
    """Generates a YouTube search URL for a given song title and artist."""
    query = f"{song_title} {artist}".strip()
    base_url = "https://www.youtube.com/results?search_query="
    return base_url + urllib.parse.quote_plus(query)

def display_song_with_link(song_title, artist):
    """Displays a song title and artist with a link to search the song on YouTube."""
    youtube_url = generate_youtube_search_url(song_title, artist)
    st.markdown(f"**{song_title} by {artist}** [Listen on YouTube]({youtube_url})", unsafe_allow_html=True)

def generate_gpt_playlist_for_vibe(vibe):
    """Generates a playlist for a given vibe using GPT-4."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": "Generate a playlist including song titles and artists based on the given vibe."},
                {"role": "user", "content": vibe}
            ]
        )
        playlist_content = response.choices[0].message['content'].strip()
        st.success('Here are your recommendations:')
        for line in playlist_content.split('\n'):
            if ' - ' in line:
                parts = line.split(' - ')
                if len(parts) >= 2:
                    song_title, artist = parts[0], parts[1]
                    display_song_with_link(song_title, artist)
            else:
                st.write(line)  # Handle contextual or descriptive lines
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def fetch_samples_with_perplexity(song_title):
    """Fetches sample information for a song using Perplexity."""
    headers = {'Authorization': f'Bearer {perplexity_api_key}', 'Content-Type': 'application/json'}
    payload = {
        "model": "sonar-medium-online",
        "messages": [
            {"role": "system", "content": "Identify songs that sample this track, including titles and artists."},
            {"role": "user", "content": song_title}
        ]
    }
    response = requests.post('https://api.perplexity.ai/v1/chat/completions', headers=headers, json=payload)
    if response.status_code == 200:
        sample_info = response.json()['choices'][0]['message']['content']
        st.success('Here are the samples found:')
        for line in sample_info.split('\n'):
            if ' - ' in line:
                parts = line.split(' - ')
                if len(parts) >= 2:
                    song_title, artist = parts[0].strip(), parts[1].strip()
                    display_song_with_link(song_title, artist)
            else:
                st.write(line)  # For non-song lines or when unable to parse details
    else:
        st.error("Failed to fetch samples: " + response.text)

# UI setup for input and option selection
option = st.selectbox("Choose your option:", ["Sample Train", "Vibe"], index=1)
input_text = st.text_input("Enter a source song or describe your vibe:")

if st.button("Discover Songs"):
    if not input_text:
        st.warning("Please enter the required information.")
    elif option == "Vibe":
        with st.spinner('Generating a vibe playlist...'):
            generate_gpt_playlist_for_vibe(input_text)
    elif option == "Sample Train":
        with st.spinner('Identifying sample-based songs...'):
            fetch_samples_with_perplexity(input_text)
