import streamlit as st
import requests
import openai

# Setup API keys
perplexity_api_key = st.secrets["perplexity"]["api_key"]
openai_api_key = st.secrets["openai"]["api_key"]

openai.api_key = openai_api_key

def call_perplexity_api(topic, content_type):
    # Adjust the query based on the content type (news or playlist)
    if content_type == "news":
        query = f"Give me detailed news stories about {topic} including direct URLs to the source."
    elif content_type == "playlist":
        query = f"Give me music playlist suggestions for a vibe related to {topic} including URLs."
    
    url = 'https://api.perplexity.ai/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {perplexity_api_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    payload = {
        "model": "gpt-4-0125-preview",
        "messages": [
            {"role": "system", "content": "You're a knowledgeable assistant tasked with providing detailed responses including source links."},
            {"role": "user", "content": query}
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
    name = st.text_input("Name")
    vibe_or_topic = st.text_input("Vibe or News Topic", help="Enter a vibe for playlists or topic for news.")
    content_type = st.radio("Content Type", ("news", "playlist"), index=0)
    submitted = st.form_submit_button("Submit")

if submitted:
    with st.spinner('Fetching your personalized content...'):
        content = call_perplexity_api(vibe_or_topic, content_type)
        
        # Optional: Refine content with GPT-4 for readability
        refined_content = refine_content_with_gpt(content)

    st.success('Content fetched successfully!')
    
    if content_type == "news":
        st.subheader('Latest News')
    else:
        st.subheader('Music Playlist Suggestions')
    st.write(refined_content)