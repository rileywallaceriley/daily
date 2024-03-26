import streamlit as st
import requests
import urllib.parse
import openai

# Display the header image
st.image("https://i.ibb.co/k6cychT/5-C4-FF130-FFD7-4860-B75-F-B442-EB296911.jpg")

# Assuming API keys are stored in Streamlit's secrets for security
perplexity_api_key = st.secrets["perplexity"]["api_key"]
openai_api_key = st.secrets["openai"]["api_key"]

# Set the OpenAI API key for usage in calls
openai.api_key = openai_api_key

def generate_youtube_search_url(song_title, artist):
    """Generates a YouTube search URL for the given song title and artist."""
    query = f"{song_title} {artist}"  # Combine song title and artist for the query
    base_url = "https://www.youtube.com/results?search_query="
    return base_url + urllib.parse.quote(query)

def display_song_with_link(song_title, artist):
    """Displays a song title and artist with a link to search the song on YouTube."""
    youtube_url = generate_youtube_search_url(song_title, artist)
    st.markdown(f"**{song_title} by {artist}** [Listen on YouTube]({youtube_url})", unsafe_allow_html=True)

def generate_gpt_playlist_for_vibe(vibe):
    """Generates a playlist for a given vibe using GPT-4."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Specify the correct GPT-4 model identifier if necessary
            messages=[
                {"role": "system", "content": "Generate a playlist for the given vibe, including song titles and artists."},
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
        # For "Sample Train" option, you would integrate a similar call to Perplexity API
        # Ensure to implement and call that function here if selecting "Sample Train"
        
        if result:
            st.success('Here are your recommendations:')
            # Assuming the result is a string with song titles and artists separated by new lines
            for line in result.split('\n'):
                if ' by ' in line:  # Basic check for expected format "Title by Artist"
                    song_title, artist = line.split(' by ', 1)
                    display_song_with_link(song_title, artist)
                else:
                    st.write(line)  # Handles lines not matching the expected format
        else:
            st.error("Unable to fetch recommendations. Please try again later or modify your input.")