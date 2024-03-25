import streamlit as st
import requests
import openai

# Setup for API keys from Streamlit's secrets
perplexity_api_key = st.secrets["perplexity"]["api_key"]
openai_api_key = st.secrets["openai"]["api_key"]

openai.api_key = openai_api_key

def call_perplexity_api(topic):
    url = 'https://api.perplexity.ai/chat/completions'
    headers = {
        'Authorization': f'Bearer {perplexity_api_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    payload = {
        "model": "mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content": topic}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Failed with status code {response.status_code}: {response.text}"

def refine_content_with_gpt(raw_content):
    try:
        response = openai.Completion.create(
            model="text-davinci-004",  # Ensure this is the correct GPT-4 model you have access to
            prompt=f"Refine and format this content: \"{raw_content}\"",
            temperature=0.5,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        # Adjusting the response parsing based on the new interface
        return response['choices'][0]['text'].strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit app layout
st.title('Your Daily Digest and Playlist')

with st.form("user_input"):
    name = st.text_input("Name")
    vibe = st.text_input("Vibe")
    astro_sign = st.selectbox("Astrological Sign", ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"])
    interests = st.multiselect("Select your interests", ["Positive News", "AI and Tech", "Gossip", "Hip-Hop"])
    submitted = st.form_submit_button("Submit")

if submitted:
    with st.spinner('Fetching your personalized content...'):
        # Fetch horoscope
        horoscope_raw = call_perplexity_api(f"horoscope for {astro_sign}")
        horoscope = refine_content_with_gpt(horoscope_raw)
        
        # Fetch news based on interests
        news_stories = [call_perplexity_api(f"latest news on {topic}") for topic in interests]
        refined_news_stories = [refine_content_with_gpt(story) for story in news_stories]
        
        # Fetch music playlist based on vibe
        playlist_raw = call_perplexity_api(f"music playlist for vibe {vibe}")
        playlist = refine_content_with_gpt(playlist_raw)

    st.success('Here’s what we found for you!')
    
    st.subheader('Your Personalized Horoscope')
    st.write(horoscope)

    if refined_news_stories:
        st.subheader('Latest News For You')
        for story in refined_news_stories:
            st.write(story)
    
    st.subheader('Your Music Playlist Recommendations')
    st.write(playlist)
