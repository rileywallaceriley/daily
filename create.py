import streamlit as st
import urllib.parse
import requests  # Make sure requests is installed
import openai

# Display the header image
st.image("https://i.ibb.co/k6cychT/5-C4-FF130-FFD7-4860-B75-F-B442-EB296911.jpg")

# Assuming API keys are stored in Streamlit's secrets for security
perplexity_api_key = st.secrets["perplexity"]["api_key"]
openai_api_key = st.secrets["openai"]["api_key"]

# Set the OpenAI API key for usage in calls
openai.api_key = openai_api_key

# Set headers for Perplexity API
headers = {
    'Authorization': f'Bearer {perplexity_api_key}',
    'Content-Type': 'application/json',
}

def generate_youtube_search_url(song_title, artist=""):
    """Generates a YouTube search URL."""
    query = f"{song_title} {artist}".strip()
    base_url = "https://www.youtube.com/results?search_query="
    return base_url + urllib.parse.quote(query)

def display_song_with_link(line):
    """Displays song details with a YouTube link."""
    song_info = line.split(' by ')
    if len(song_info) >= 2:
        song_title, artist_info = song_info[0], ' by '.join(song_info[1:])
        youtube_url = generate_youtube_search_url(song_title, artist_info.split(' ft.')[0].split(',')[0])
        st.markdown(f"**{song_title}** by {artist_info} [Listen on YouTube]({youtube_url})", unsafe_allow_html=True)
    else:
        st.write(line)

def call_perplexity_api_for_samples(input_text):
    """Identifies songs that sample another song using Perplexity."""
    payload = {
        "model": "sonar-medium-online",  # Model based on your example
        "messages": [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content": f"Identify songs that sample '{input_text}'."}
        ]
    }
    response = requests.post('https://api.perplexity.ai/chat/completions', headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Failed with status code {response.status_code}: {response.text}"

# UI setup for input and button to generate playlist or identify samples
option = st.selectbox("Choose your option:", ["Sample Train", "Vibe"], index=1)
input_text = st.text_input("Enter a source song or describe your vibe:")

if st.button("Discover Songs"):
    if not input_text:
        st.warning("Please enter the required information.")
    else:
        result = None
        if option == "Vibe":
            with st.spinner('Generating a vibe playlist...'):
                result = generate_gpt_playlist_for_vibe(input_text)  # This needs to be defined
        elif option == "Sample Train":
            with st.spinner('Identifying sample-based songs...'):
                result = call_perplexity_api_for_samples(input_text)

        if result:
            st.success('Here are your recommendations:')
            for line in result.split('\n'):
                if line.strip():  # Check if line is not empty
                    display_song_with_link(line.strip())
        else:
            st.error("Unable to fetch recommendations. Please try again.")
