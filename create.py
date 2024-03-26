import streamlit as st
import openai
import random
import urllib.parse

# Function to generate a random image only once per session
def get_random_image():
    if 'image_url' not in st.session_state:
        image_urls = [
            "https://i.ibb.co/BNHvHM0/684518-B3-B7-D0-45-D7-8801-2355-D70-D169-C.webp",
            "https://i.ibb.co/LJQZ9s7/33540-C0-B-E7-DE-48-CC-AA39-64-BA2-E57-B264.jpg",
            "https://i.ibb.co/gZ0wVhR/24-E8737-A-108-A-4-FB6-81-A8-34566-DA12-CCA.jpg",
            "https://i.ibb.co/k6cychT/5-C4-FF130-FFD7-4860-B75-F-B442-EB296911.jpg"
        ]
        st.session_state['image_url'] = random.choice(image_urls)
    return st.session_state['image_url']

# Display the header image using session state to keep it constant across interactions
st.image(get_random_image())

# Contextual text under the image
st.write("Welcome to Vibe Cat; give me your vibe (a song you love, a feeling, etc.) and I'll curate a great playlist.")

# Assuming API keys are stored in Streamlit's secrets for security
openai_api_key = st.secrets["openai"]["api_key"]

# Set the OpenAI API key for usage in calls to GPT-4
openai.api_key = openai_api_key

# Rest of the script for input handling, checkboxes, and playlist generation remains unchanged...

if st.button("Curate Playlist"):
    if not input_text:
        st.warning("Please enter the required information.")
    else:
        with st.spinner('Curating your playlist...'):
            generate_gpt_playlist(input_text, include_top_40, stay_super_random)
