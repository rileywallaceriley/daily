import streamlit as st
import requests
import urllib.parse

# Assuming API keys are stored in Streamlit's secrets
perplexity_api_key = st.secrets["perplexity"]["api_key"]

def call_perplexity_api(option, input_text):
    url = 'https://api.perplexity.ai/chat/completions'
    headers = {
        'Authorization': f'Bearer {perplexity_api_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    query_content = "List songs based on '{}' with titles, artists, and years.".format(input_text) if option == "Vibe" else "List songs sampled in '{}' with titles, artists, and years.".format(input_text)
    payload = {
        "model": "sonar-medium-online",  # Adjust according to the available models
        "messages": [
            {"role": "system", "content": "You're a knowledgeable assistant tasked with providing song titles, artists, and years."},
            {"role": "user", "content": query_content}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return "Failed with status code {}: {}".format(response.status_code, response.text)

def generate_youtube_search_url(song_title):
    base_url = "https://www.youtube.com/results?search_query="
    query = urllib.parse.quote(song_title)
    return base_url + query

# Streamlit app layout
st.title('Music Exploration Assistant')

option = st.selectbox("Choose your option:", ["Sample Train", "Vibe"], index=1)
input_text = st.text_input("Enter a source song or describe your vibe:")

if st.button("Discover Songs"):
    if not input_text:
        st.warning("Please enter the required information.")
    else:
        with st.spinner('Fetching songs...'):
            song_details = call_perplexity_api(option, input_text)
            
            if song_details:
                st.success('Check out these tunes!')
                for detail in song_details.split('\n'):  # Assuming each song detail is separated by a newline
                    if detail.strip():  # Check if the detail line is not empty
                        # Assuming the title and artist are sufficient for YouTube search
                        title, artist = detail.split(', ')[:2]  # Safely unpack first two elements
                        youtube_url = generate_youtube_search_url(f"{title} {artist}")
                        st.markdown("Title: **{}**".format(title))
                        st.markdown("Artist: **{}**".format(artist))
                        st.markdown("[Click here to listen]({})".format(youtube_url))
            else:
                st.error("Unable to fetch recommendations. Try tweaking your input.")