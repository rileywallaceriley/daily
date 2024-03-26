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
    if option == "Sample Train":
        query_content = f"List songs sampled in '{input_text}'. Provide song titles."
    else:  # Vibe
        query_content = f"Based on the vibe '{input_text}', list songs that fit. Provide song titles."

    payload = {
        "model": "sonar-medium-online",  # Adjust model if necessary
        "messages": [
            {"role": "system", "content": "You're a knowledgeable assistant tasked with providing song titles."},
            {"role": "user", "content": query_content}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Failed with status code {response.status_code}: {response.text}"

def generate_youtube_search_url(song_title):
    base_url = "https://www.youtube.com/results?search_query="
    query = urllib.parse.quote(song_title)
    return base_url + query

# Streamlit app layout
st.title('Music Recommendation and YouTube Search Generator')

option = st.selectbox("Choose your option:", ["Sample Train", "Vibe"], index=1)
input_text = st.text_input("Enter a source song or describe your vibe:")

if st.button("Generate Recommendations"):
    if not input_text:
        st.warning("Please enter the required information.")
    else:
        with st.spinner('Fetching recommendations...'):
            recommendations = call_perplexity_api(option, input_text)
            st.success('Recommendations fetched successfully!')
            st.write("Recommendations:")
            st.write(recommendations)  # Display raw recommendations for context

            # Assuming recommendations are separated by lines or a specific delimiter
            songs = recommendations.split('\n')  # Adjust based on actual format
            st.write("YouTube Search URLs:")
            for song in songs:
                if song.strip():  # Ensure the song title isn't empty
                    url = generate_youtube_search_url(song.strip())
                    st.markdown(f"[{song}]({url})", unsafe_allow_html=True)