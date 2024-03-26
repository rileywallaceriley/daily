import streamlit as st
import requests
import urllib.parse

# Assuming API keys are stored in Streamlit's secrets
perplexity_api_key = st.secrets["perplexity"]["api_key"]

def call_perplexity_api(option, input_text):
    """
    Adjusted to ask Perplexity for detailed information.
    """
    url = 'https://api.perplexity.ai/chat/completions'
    headers = {
        'Authorization': f'Bearer {perplexity_api_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    query_content = f"Provide detailed song recommendations based on '{input_text}'." if option == "Vibe" else f"List songs sampled in '{input_text}' with details."

    payload = {
        "model": "sonar-medium-online",
        "messages": [
            {"role": "system", "content": "You're tasked with providing detailed song recommendations including title, artist, producer, album, year, and a short blurb."},
            {"role": "user", "content": query_content}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Failed with status code {response.status_code}: {response.text}"

def generate_youtube_search_url(song_title):
    base_url = "https://www.youtube.com/results?search_query="
    query = urllib.parse.quote(song_title)
    return base_url + query

def generate_intro(input_text, option):
    """
    Generates an engaging introduction in a knowledgeable tone.
    """
    base_intro = "Alright, let's dive into this journey through sound."
    if option == "Vibe":
        return f"{base_intro} You're feeling '{input_text}', which is absolutely a vibe I can get behind. Here's a playlist that perfectly captures that essence. Each song is a little exploration into the mood you're seeking."
    else:  # Sample Train
        return f"{base_intro} Diving into the roots of '{input_text}' is like exploring a treasure map of music history. Here's a list showcasing the impact of this song across the soundscape. It's fascinating to see the ripples it created."

# Streamlit app layout
st.title('Your Curated Music Experience')

option = st.selectbox("Choose your option:", ["Sample Train", "Vibe"], index=1)
input_text = st.text_input("Enter a source song or describe your vibe:")

if st.button("Generate Recommendations"):
    if not input_text:
        st.warning("Please enter the required information.")
    else:
        intro = generate_intro(input_text, option)
        st.markdown(f"### {intro}")
        
        with st.spinner('Fetching recommendations...'):
            recommendations = call_perplexity_api(option, input_text)
            
            if recommendations:
                st.success('Check out these tunes!')
                # Example recommendation format handling
                # This part needs adjustment based on the actual format of Perplexity's response
                for rec in recommendations.split('\n\n'):  # Assuming each rec is separated by two newlines
                    details, blurb = rec.split('\n', 1)  # Splitting details from the blurb
                    title, artist, producer, album, year = details.split(', ')  # Example parsing
                    youtube_url = generate_youtube_search_url(f"{title} {artist}")
                    st.markdown(f"""
                    **Title:** {title}  
                    **Artist:** {artist}  
                    **Producer:** {producer}  
                    **Album:** {album}  
                    **Year:** {year}  
                    **About:** {blurb}  
                    [Click here to listen]({youtube_url})
                    """)
            else:
                st.error("Failed to fetch recommendations. Try tweaking your input.")