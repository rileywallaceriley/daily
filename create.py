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

def call_perplexity_api(input_text):
    url = 'https://api.perplexity.ai/chat/completions'
    headers = {
        'Authorization': f'Bearer {perplexity_api_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    payload = {
        "model": "sonar-medium-online",
        "messages": [
            {"role": "system", "content": "You're a knowledgeable assistant tasked with providing song titles, artists, and years that sampled another song."},
            {"role": "user", "content": f"Which songs sampled '{input_text}'?"}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Failed to fetch recommendations due to an error: {response.text}"

def generate_gpt_playlist(vibe):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": "You are a highly creative AI, familiar with music across genres. Generate a playlist based on a given vibe, including song titles, artists, and YouTube links."},
                {"role": "user", "content": f"Create a playlist for the vibe: '{vibe}'."}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

def display_songs(response_text):
    if response_text.strip():
        songs = response_text.split('\n')
        for song in songs:
            if song.strip():
                youtube_url = generate_youtube_search_url(song)
                st.markdown(f"- {song} [Listen on YouTube]({youtube_url})", unsafe_allow_html=True)
    else:
        st.write("The response did not contain any song information.")

# Streamlit UI
st.title('Music Exploration Assistant')

option = st.selectbox("Choose your option:", ["Sample Train", "Vibe"], index=1)
input_text = st.text_input("Enter a source song or describe your vibe:")

if st.button("Discover Songs"):
    if not input_text:
        st.warning("Please enter the required information.")
    else:
        result = ""
        if option == "Sample Train":
            with st.spinner('Fetching songs based on sample...'):
                result = call_perplexity_api(input_text)
        else:  # Vibe
            with st.spinner('Generating a vibe playlist...'):
                result = generate_gpt_playlist(input_text)
                
        if result and not result.startswith("Failed"):
            st.success('Here are your recommendations:')
            display_songs(result)
        else:
            st.error(result)  # Display the error message directly