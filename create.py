import streamlit as st
import requests
import urllib.parse
import openai

# Display the header image
st.image("https://i.ibb.co/k6cychT/5-C4-FF130-FFD7-4860-B75-F-B442-EB296911.jpg")

# Assuming API keys are stored in Streamlit's secrets
perplexity_api_key = st.secrets["perplexity"]["api_key"]
openai_api_key = st.secrets["openai"]["api_key"]

# Set the OpenAI API key for usage in calls
openai.api_key = openai_api_key

def generate_youtube_search_url(song_title, artist):
    """Generates a YouTube search URL for the given song title and artist."""
    query = f"{song_title} {artist}"  # Combine song title and artist for the query
    base_url = "https://www.youtube.com/results?search_query="
    return base_url + urllib.parse.quote(query)

def display_song_with_brief_and_link(song_title, artist, brief):
    """Displays a song title, artist, a brief description, and a YouTube link."""
    youtube_url = generate_youtube_search_url(song_title, artist)
    # Display song title and artist bolder and larger, followed by a brief and the YouTube link
    st.markdown(f"**{song_title} by {artist}** - {brief} [Listen on YouTube]({youtube_url})", unsafe_allow_html=True)

def generate_gpt_playlist_for_vibe(vibe):
    """Generates a playlist for a given vibe using the specified GPT-4 model."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-0125-preview",  # Specified GPT-4 model
            messages=[
                {"role": "system", "content": "Generate a playlist for the given vibe, including song titles, artists, and a brief description for each."},
                {"role": "user", "content": vibe}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# UI setup for option selection and input
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
        # For "Sample Train", implement similar logic as "Vibe" using Perplexity

        if result:
            st.success('Here are your recommendations:')
            for line in result.split('\n'):
                # Parsing each line for title, artist, and brief assuming a specific format
                parts = line.split(' - ', 2)  # Splitting on ' - ' which separates the song from its brief
                if len(parts) >= 3:
                    song_title, artist, brief = parts[0], parts[1], parts[2]
                    display_song_with_brief_and_link(song_title, artist, brief)
                else:
                    st.write("Song format not recognized or brief missing.")
        else:
            st.error("Unable to fetch recommendations. Please try again later or modify your input.")