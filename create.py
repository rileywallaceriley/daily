import streamlit as st
import urllib.parse
import requests
import openai

# Display the header image at the top of the app
st.image("https://i.ibb.co/k6cychT/5-C4-FF130-FFD7-4860-B75-F-B442-EB296911.jpg")

# Assuming API keys are stored in Streamlit's secrets for security
perplexity_api_key = st.secrets["perplexity"]["api_key"]
openai_api_key = st.secrets["openai"]["api_key"]

# Set the OpenAI API key for usage in calls to GPT-4
openai.api_key = openai_api_key

def generate_youtube_search_url(song_title, artist=""):
    """Generates a YouTube search URL for a given song title and artist."""
    query = f"{song_title} {artist}".strip()
    base_url = "https://www.youtube.com/results?search_query="
    return base_url + urllib.parse.quote(query)

def display_song_with_link(line):
    """Displays a song title and artist with a link to search the song on YouTube."""
    song_info = line.split(' - ')
    if len(song_info) >= 2:
        song_title, artist = song_info[0], ' - '.join(song_info[1:])
        youtube_url = generate_youtube_search_url(song_title, artist)
        st.markdown(f"**{song_title} by {artist}** [Listen on YouTube]({youtube_url})", unsafe_allow_html=True)
    else:
        st.write(line)  # For non-song lines or when unable to parse song details

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
        return response.choices[0].message['content'].strip()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def call_perplexity_api_for_samples(topic):
    """Calls the Perplexity API to identify songs that sample another song."""
    headers = {
        'Authorization': f'Bearer {perplexity_api_key}',
        'Content-Type': 'application/json',
    }
    payload = {
        "model": "mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content": topic}
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
                result = generate_gpt_playlist_for_vibe(input_text)
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
