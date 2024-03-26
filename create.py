import streamlit as st
import requests
import urllib.parse

# Assuming API keys are stored in Streamlit's secrets for security
perplexity_api_key = st.secrets["perplexity"]["api_key"]

def call_perplexity_api(option, input_text):
    url = 'https://api.perplexity.ai/chat/completions'
    headers = {
        'Authorization': f'Bearer {perplexity_api_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    # Tailoring the query based on the selected option
    query_content = f"List songs based on '{input_text}' with titles and artists." if option == "Vibe" else f"List songs sampled in '{input_text}' with titles and artists."
    payload = {
        "model": "sonar-medium-online",  # Utilize the specified model for queries
        "messages": [
            {"role": "system", "content": "You're a knowledgeable assistant tasked with providing song titles and artists."},
            {"role": "user", "content": query_content}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return "Failed to fetch recommendations due to an error."

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
            
            if song_details and song_details.startswith("Failed to fetch"):
                st.error(song_details)  # Display the error message directly if any
            elif song_details:
                st.success('Check out these tunes!')
                for detail in song_details.split('\n'):  # Assuming each song detail is separated by a newline
                    if detail.strip():  # Ensures detail is not empty
                        parts = detail.split(', ')
                        if len(parts) >= 2:  # Expecting at least title and artist
                            title, artist = parts[0], parts[1]
                            youtube_url = generate_youtube_search_url(f"{title} {artist}")
                            st.write(f"**Title:** {title}, **Artist:** {artist}")
                            st.markdown(f"[Click here to listen]({youtube_url})", unsafe_allow_html=True)
                        else:
                            st.write("Missing some information for a song.")
            else:
                st.error("No recommendations found. Try a different query.")