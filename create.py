import streamlit as st
import requests
from openai import ChatCompletion
import pandas as pd
from bs4 import BeautifulSoup  # Import for HTML parsing

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
    "model": "sonar-medium-online",  # Using the specified model
    "messages": [
      {"role": "system", "content": "You're a knowledgeable assistant tasked with providing personalized horoscopes, detailed news stories and playlists including source links."},
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
    response = ChatCompletion.create(
      model="gpt-4-0125-preview",
      messages=[
        {"role": "system", "content": "You are an AI who formats provided content into a concise, readable format for web display, ensuring to retain all original details and links."},
        {"role": "user", "content": content}
      ]
    )
    return response['choices'][0]['message']['content'].strip()
  except Exception as e:
    return f"An error occurred: {str(e)}"

def get_news_headlines():
  # Define websites and limit the number of stories per website (max 2)
  websites = [
    "https://hiphopdx.com/news/",
    "https://mashable.com/",
    "https://www.theverge.com/",
    "https://futurism.com/the-byte",
    "https://www.positive.news/"
  ]
  all_stories = []
  for website in websites:
    response = requests.get(website)
    soup = BeautifulSoup(response.content, 'html.parser')  # Assuming HTML parsing
    # Extract headlines and limit to 2 per website
    for story in soup.find_all('h2')[:2]:
      link = story.find('a')['href']
      text = story.text.strip()
      all_stories.append((text, link, website))
  # Sort by estimated user interest (perplexity might be suitable here)
  # For simplicity, assuming a random sort here
  random.shuffle(all_stories)
  # Select top 6 stories
  return all_stories[:6]

def get_horoscope(astrological_sign):
  # Use perplexity to get a personalized horoscope based on the sign
  prompt = f"Today's horoscope for someone born under the sign of {astrological_sign}"
  horoscope_text = call_perplexity_api(prompt)
  # Refine the horoscope text for better readability
  return refine_content_with_gpt(horoscope_text)

# Streamlit app layout
st.title('Your Daily Digest and Playlist Generator')

# Use a dropdown for astrological sign selection
selected_sign = st.selectbox(
  "Your Astrological Sign",
  ("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio",
   "Sagittarius", "Capricorn", "Aquarius", "Pisces")
)

# Remove user input for news topic and vibe
# Vibe information might be useful for playlist later
with st.spinner('Fetching your personalized content...'):
  # Get horoscope
  horoscope = get_horoscope(selected_sign)
   # Get top news stories
  news_stories = get_news_headlines()
  news_df = pd.DataFrame(news_stories, columns=["Headline", "Link", "Source"])

  # Placeholder for playlist generation based on vibe (uncomment and implement)
  # vibe = st.text_input("Vibe", help="Describe the vibe for your music playlist.")
  # playlist = call_perplexity_api(f"music playlist suggestions for a {vibe} vibe including source links")
  # refined_playlist = refine_content_with_gpt(playlist)

  st.success('Content fetched successfully!')

  # Display Horoscope
  st.subheader('Your Horoscope for Today')
  st.write(horoscope)

  # Display News Stories
  st.subheader('Top News Stories')
  st.write(news_df.to_string(index=False))  # Optionally format the output

# This line needs to be indented outside the with statement
st.stop()
