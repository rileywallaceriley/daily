import streamlit as st
import requests

# Assuming API keys are stored in Streamlit's secrets
perplexity_api_key = st.secrets["perplexity"]["api_key"]

def call_perplexity_api(option, input_text):
    url = 'https://api.perplexity.ai/chat/completions'
    headers = {
        'Authorization': f'Bearer {perplexity_api_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    # Adjusting the payload based on the user's choice
    if option == "Sample Train":
        query_content = f"Give me a list of songs sampled in the song {input_text} with YouTube links."
    else:  # Vibe
        query_content = f"Based on feeling {input_text}, suggest a perfect playlist with YouTube links."
    
    payload = {
        "model": "sonar-medium-online",
        "messages": [
            {"role": "system", "content": "You're a knowledgeable assistant tasked with providing detailed playlists including source links."},
            {"role": "user", "content": query_content}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Failed with status code {response.status_code}: {response.text}"

# Streamlit app layout
st.title('Music Playlist Generator')

# Dropdown for user to choose between Sample Train or Vibe
option = st.selectbox("Choose your option:", ["Sample Train", "Vibe"])

input_text = ""
if option == "Sample Train":
    input_text = st.text_input("Enter a source song:")
elif option == "Vibe":
    input_text = st.text_input("How are you feeling?")

if st.button("Submit"):
    if not input_text:
        st.write("Please enter the required information.")
    else:
        with st.spinner('Fetching your personalized playlist...'):
            playlist_content = call_perplexity_api(option, input_text)
            st.success('Playlist fetched successfully!')
            st.write(playlist_content)