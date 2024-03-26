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
    query_content = f"List songs based on '{input_text}' with titles, artists, and years." if option == "Vibe" else f"List songs sampled in '{input_text}' with titles, artists, and years."
    payload = {
        "model": "sonar-medium-online",
        "messages": [
            {"role": "system", "content": "You're a knowledgeable assistant tasked with providing song titles, artists, and years."},
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

def generate_intro(input_text, option):
    base_intro = "Alright, diving into this musical journey."
    if option == "Vibe":
        return f"{base_intro} Feeling '{input_text}' is the perfect prompt for discovering some tunes. Here's what aligns with your vibe:"
    else:
        return f"{base_intro} Exploring the tracks that sampled '{input_text}' opens up a fascinating sonic web. Check these out:"

# Streamlit app layout
st.title('Music Exploration Assistant')

option = st.selectbox("Choose your option:", ["Sample Train", "Vibe"], index=1)
input_text = st.text_input("Enter a source song or describe your vibe:")

if st.button("Discover Songs"):
    if not input_text:
        st.warning("Please enter the required information.")
    else:
        intro = generate_intro(input_text, option)
        st.markdown(f"### {intro}")
        
        with st.spinner('Fetching songs...'):
            song_details = call_perplexity_api(option, input_text)
            
            # Assuming song details are separated by a specific delimiter
             for detail in song_details.split('\n'):  # Adjust based on the actual format of the response
    if detail.strip():  # Check if the detail line is not empty
        # Simple parsing for title, artist, and year
        parts = detail.split(', ')
        if len(parts) >= 3:
            title, artist, year = parts[0], parts[1], parts[2]
            youtube_url = generate_youtube_search_url(f"{title} {artist}")
            
            # Displaying each song detail followed by the raw YouTube URL
            st.write(f"Title: {title}")
            st.write(f"Artist: {artist}")
            st.write(f"Year: {year}")
            st.write("Click here to listen:", youtube_url)
        else:
            st.write("Missing some information for a song.")