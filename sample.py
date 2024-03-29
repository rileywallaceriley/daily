import os
import requests
import streamlit as st
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

perplexity_api_key = os.getenv('PERPLEXITY_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')

if perplexity_api_key is None or openai_api_key is None:
    st.error("API keys not found. Please set the PERPLEXITY_API_KEY and OPENAI_API_KEY environment variables.")
else:
    # Streamlit app interface
    st.title('Sample Explorer')

    # User inputs for song and artist
    song = st.text_input('Enter the song title:')
    artist = st.text_input('Enter the artist name:')

    if st.button('Find Samples'):
        if song and artist:
            # Formulating the query for real-time data from Perplexity
            query = f"Provide real-time information on the samples used in '{song}' by {artist}."

            # Setting up the Perplexity API request
            url = 'https://api.perplexity.ai/chat/completions'
            headers = {
                'Authorization': f'Bearer {perplexity_api_key}',
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
                # Extracting the insight from Perplexity
                perplexity_insights = response.json()['choices'][0]['message']['content']
                
                # Now formatting with GPT-4
                openai.api_key = openai_api_key
                gpt_prompt = f"Format the following information into a concise summary: {perplexity_insights}\n\nGenerate a YouTube search link for the song '{song}' by {artist}."

                try:
                    gpt_response = openai.Completion.create(
                        model="text-davinci-003",
                        prompt=gpt_prompt,
                        temperature=0.5,
                        max_tokens=150
                    )
                    formatted_text = gpt_response.choices[0].text.strip()
                    st.markdown(formatted_text)
                except Exception as e:
                    st.error(f"An error occurred with GPT-4: {str(e)}")
            else:
                st.error(f"Failed with status code {response.status_code}: {response.text}")
        else:
            st.warning('Please enter both a song title and an artist name to find samples.')