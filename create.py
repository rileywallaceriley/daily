import streamlit as st
import requests
import urllib.parse
import openai

# Assuming API keys are stored in Streamlit's secrets
perplexity_api_key = st.secrets["perplexity"]["api_key"]
openai_api_key = st.secrets["openai"]["api_key"]

openai.api_key = openai_api_key

def call_perplexity_api(input_text):
    """
    Use Perplexity for identifying songs based on samples.
    """
    url = 'https://api.perplexity.ai/chat/completions'
    headers = {
        'Authorization': f'Bearer {perplexity_api_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    payload = {
        "model": "sonar-medium-online",
        "messages": [
            {"role": "system", "content": "You're a knowledgeable assistant tasked with providing detailed information on songs that sample another song."},
            {"role": "user", "content": f"Which songs sample '{input_text}'?"}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return "Failed to fetch recommendations due to an error."

def generate_gpt_playlist(vibe):
    """
    Leverage GPT-4 for generating vibe-based playlists, including YouTube links.
    Adjust the engine parameter to match the specific GPT-4 model you have access to.
    """
    try:
        response = openai.Completion.create(
            engine="gpt-4-0125-preview",  # Adjust to the specific GPT-4 model you're using
            prompt=f"Create a playlist for the vibe: '{vibe}'. Include song titles, artists, and YouTube links.",
            temperature=0.7,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"
        
# Streamlit UI
st.title('Music Exploration Assistant')

option = st.selectbox("Choose your option:", ["Sample Train", "Vibe"], index=1)
input_text = st.text_input("Enter a source song or describe your vibe:")

if st.button("Discover Songs"):
    if not input_text:
        st.warning("Please enter the required information.")
    else:
        if option == "Sample Train":
            with st.spinner('Fetching songs based on sample...'):
                result = call_perplexity_api(input_text)
        else:  # Vibe
            with st.spinner('Generating a vibe playlist...'):
                result = generate_gpt_playlist(input_text)
                
        if result:
            st.success('Here are your recommendations:')
            st.write(result)
        else:
            st.error("Unable to fetch recommendations. Please try again later or modify your input.")