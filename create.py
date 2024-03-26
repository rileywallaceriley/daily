import streamlit as st
import urllib.parse
import openai
import requests  # Ensure requests is installed for Perplexity API calls

# Display the header image
st.image("https://i.ibb.co/k6cychT/5-C4-FF130-FFD7-4860-B75-F-B442-EB296911.jpg")

# Assuming API keys are stored in Streamlit's secrets for security
perplexity_api_key = st.secrets["perplexity"]["api_key"]
openai_api_key = st.secrets["openai"]["api_key"]

# Set the OpenAI API key for usage in calls
openai.api_key = openai_api_key

def generate_youtube_search_url(song_title, artist=""):
    """Generates a YouTube search URL."""
    query = f"{song_title} {artist}".strip()
    base_url = "https://www.youtube.com/results?search_query="
    return base_url + urllib.parse.quote(query)

def display_song_with_link(line):
    """Displays song details with a YouTube link or regular text for non-song lines."""
    song_info = line.split(' by ')
    if len(song_info) >= 2:
        song_title, artist_info = song_info[0], ' by '.join(song_info[1:])
        youtube_url = generate_youtube_search_url(song_title, artist_info.split(' ft.')[0].split(',')[0])
        st.markdown(f"**{song_title}** by {artist_info} [Listen on YouTube]({youtube_url})", unsafe_allow_html=True)
    else:
        st.write(line)  # Handle non-song lines or errors gracefully

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

def call_perplexity_api_for_samples(input_text):
    """Identifies songs that sample another song using Perplexity."""
    url = 'https://api.perplexity.ai/v1/chat/completions'  # Adjust as needed for Perplexity's endpoint
    headers = {
        'Authorization': f'Bearer {perplexity_api_key}',
        'Content-Type': 'application/json',
    }
    payload = {
        "model": "sonar-medium-online",  # Adjust based on available models and your requirement
        "prompt": f"Identify songs that sample '{input_text}'.",
        "temperature": 0.7,
        "max_tokens": 1000
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get('choices', [{}])[0].get('message', {}).get('content', '').strip()
    else:
        st.error("Failed to fetch samples due to an error.")
        return None

# Streamlit UI for input and button to generate playlist or samples
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
                display_song_with_link(line.strip())
        else:
            st.error("Unable to fetch recommendations. Please try again.")
