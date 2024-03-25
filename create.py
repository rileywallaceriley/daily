import streamlit as st
import requests
import openai

# Assuming API keys are stored in Streamlit's secrets
perplexity_api_key = st.secrets["perplexity"]["api_key"]
openai_api_key = st.secrets["openai"]["api_key"]

# Setting the OpenAI API key for later use
openai.api_key = openai_api_key

def call_perplexity_api(topic):
    url = 'https://api.perplexity.ai/chat/completions'
    headers = {
        'Authorization': f'Bearer {perplexity_api_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
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

def fetch_news():
    # Websites to fetch news from
    websites = [
        "https://hiphopdx.com/news/",
        "https://mashable.com/",
        "https://www.theverge.com/",
        "https://futurism.com/the-byte",
        "https://www.positive.news/"
    ]
    news_items = []
    for site in websites:
        news = call_perplexity_api(f"fetch the top stories from {site}")
        news_items.extend(news.split('\n')[:2])  # Assuming the API returns a list of news items separated by newlines
    return news_items

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
st.title('Your Daily Digest, Horoscope, and Playlist Generator')

with st.form("user_input"):
    name = st.text_input("Name", help="What's your name?")
    astro_sign = st.selectbox("Astrological Sign", ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"], help="Choose your astrological sign for a personalized horoscope.")
    vibe = st.text_input("Vibe", help="Describe the vibe for your music playlist.")
    submitted = st.form_submit_button("Submit")

if submitted:
    with st.spinner('Fetching your personalized content...'):
        horoscope_content = call_perplexity_api(f"horoscope for {astro_sign} in a motivational tone")
        news_content = fetch_news()
        playlist_content = call_perplexity_api(f"music playlist suggestions for a {vibe} vibe including source links")
        
        refined_horoscope = refine_content_with_gpt(horoscope_content)
        refined_news = refine_content_with_gpt('\n'.join(news_content))
        refined_playlist = refine_content_with_gpt(playlist_content)

    st.success('Content fetched successfully!')
    
    st.subheader('Your Personalized Horoscope')
    st.write(refined_horoscope)
    
    st.subheader('Latest News')
    st.write(refined_news)

    st.subheader('Music Playlist Suggestions')
    st.write(refined_playlist)