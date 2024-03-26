import streamlit as st
import urllib.parse
import requests
import openai

# Display the header image
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
        st.write(line)

def attempt_sample_identification_with_gpt_and_perplexity(topic):
    """Attempts to identify samples with GPT, then falls back to Perplexity if needed."""
    # First, try with GPT
    gpt_response = openai.ChatCompletion.create(
        model="gpt-4-0125-preview",
        messages=[
            {"role": "system", "content": "Identify songs that sample the given song, including song titles and artists."},
            {"role": "user", "content": topic}
        ]
    )
    gpt_content = gpt_response.choices[0].message['content'].strip()
    if "I don't have that information" in gpt_content:
        # If GPT can't provide a satisfactory response, fallback to Perplexity
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
    else:
        return gpt_content

# UI setup for input and button to generate playlist or identify samples
option = st.selectbox("Choose your option:", ["Sample Train", "Vibe"], index=1)
input_text = st.text_input("Enter a source song or describe your vibe:")

if st.button("Discover Songs"):
    if not input_text:
        st.warning("Please enter the required information.")
    else:
        if option == "Vibe":
            with st.spinner('Generating a vibe playlist...'):
                playlist_content = generate_gpt_playlist_for_vibe(input_text)
                if playlist_content:
                    st.success('Here are your recommendations:')
                    for line in playlist_content.split('\n'):
                        display_song_with_link(line.strip())
                else:
                    st.error("Unable to fetch vibe playlist. Please try again.")
        elif option == "Sample Train":
            with st.spinner('Identifying sample-based songs...'):
                sample_info = attempt_sample_identification_with_gpt_and_perplexity(input_text)
                if sample_info:
                    st.success('Here are your recommendations:')
                    for line in sample_info.split('\n'):
                        if line.strip():  # Check if line is not empty
                            display_song_with_link(line.strip())
                else:
                    st.error("Unable to fetch sample information. Please try again.")
