import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv('PERPLEXITY_API_KEY')

if api_key is None:
    st.error("Perplexity API key not found. Please set the PERPLEXITY_API_KEY environment variable.")
else:
    # Streamlit app interface
    st.title('Sample Explorer')

    # User inputs for song and artist
    song = st.text_input('Enter the song title:')
    artist = st.text_input('Enter the artist name:')

    if st.button('Find Samples'):
        if song and artist:
            # Formulating the query for real-time data
            query = f"Provide real-time information on the samples used in '{song}' by {artist}."

            # Setting up the API request
            url = 'https://api.perplexity.ai/chat/completions'
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            payload = {
                "model": "sonar-medium-online",  # Specify the model capable of real-time searches
                "messages": [
                    {
                        "role": "user",
                        "content": query
                    }
                ]
            }

            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                # Assuming the API response includes detailed information in a structured format
                # This part needs to be adjusted based on the actual structure of your API response
                data = response.json()['choices'][0]['message']['content']
                # Parse 'data' to extract relevant details
                # Here you need to adapt this logic to match the response structure of your API
                # For demonstration, let's assume 'data' contains a dict with the required info
                # This is a placeholder to show formatting; replace with real parsing logic
                details = {
                    "song_title": song,
                    "artist": artist,
                    "producers": "John Doe, Jane Smith",
                    "album": "Hits of 2024",
                    "youtube_link": "https://youtu.be/dQw4w9WgXcQ"
                }
                
                # Displaying the details in a structured format
                st.subheader(f"Details for '{details['song_title']}' by {details['artist']}")
                st.markdown(f"""
                - **Artist:** {details['artist']}
                - **Producers:** {details['producers']}
                - **Album:** {details['album']}
                - **Listen on YouTube:** [Link]({details['youtube_link']})
                """)
            else:
                st.error(f"Failed with status code {response.status_code}: {response.text}")
        else:
            st.warning('Please enter both a song title and an artist name to find samples.')