import streamlit as st
import requests
import openai

# Setup for API keys from Streamlit's secrets
perplexity_api_key = st.secrets["perplexity"]["api_key"]
openai_api_key = st.secrets["openai"]["api_key"]

# Setting the OpenAI API key
openai.api_key = openai_api_key

def call_perplexity_api(topic):
    url = 'https://api.perplexity.ai/chat/completions'
    headers = {
        'Authorization': f'Bearer {perplexity_api_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    payload = {
        "model": "sonar-medium-online",
        "messages": [
            {"role": "system", "content": "You're a knowledgeable assistant tasked with providing detailed news stories and playlists including source links."},
            {"role": "user", "content": topic}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Failed with status code {response.status_code}: {response.text}"

def refine_content_with_gpt(content):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": "You are an AI who formats provided content into a concise, readable format for web display, ensuring to retain all original details and links."},
                {"role": "user", "content": content}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit app layout
st.title('Your Daily Digest and Playlist Generator')

with st.form("user_input"):
    name = st.text_input("Name", help="What's your name?")
    topic = st.text_input("News Topic", help="Enter a topic to get the latest news.")
    vibe = st.text_input("Vibe", help="Describe the vibe for your music playlist.")
    submitted = st.form_submit_button("Submit")

if submitted:
    with st.spinner('Fetching your personalized content...'):
        # Fetch news
        news_content = call_perplexity_api(f"latest news about {topic} including source links")
        # Fetch playlist
        playlist_content = call_perplexity_api(f"music playlist suggestions for a {vibe} vibe including source links")
        
        # Refine content with GPT-4 for readability
        refined_news = refine_content_with_gpt(news_content)
        refined_playlist = refine_content_with_gpt(playlist_content)

    st.success('Content fetched successfully!')
    
    st.subheader('Latest News')
    st.write(refined_news)

    st.subheader('Music Playlist Suggestions')
    st.write(refined_playlist)