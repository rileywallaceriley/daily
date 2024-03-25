import requests
import openai

# Setup for API keys from Streamlit's secrets
# Setup API keys (Replace 'your_api_key_here' with your actual API keys stored in Streamlit secrets)
perplexity_api_key = st.secrets["perplexity"]["api_key"]
openai_api_key = st.secrets["openai"]["api_key"]

openai.api_key = openai_api_key

def call_perplexity_api(topic):
    url = 'https://api.perplexity.ai/chat/completions'
    url = 'https://api.perplexity.ai/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {perplexity_api_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    payload = {
        "model": "sonar-medium-online",
        "model": "gpt-4-0125-preview",  # Adjust based on the Perplexity's documentation
        "messages": [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "system", "content": "You're a knowledgeable assistant tasked with providing detailed news stories and playlists including source links."},
            {"role": "user", "content": topic}
        ]
    }
@@ -28,53 +28,46 @@ def call_perplexity_api(topic):
    else:
        return f"Failed with status code {response.status_code}: {response.text}"

def refine_content_with_gpt(raw_content):
def refine_content_with_gpt(content):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-0125-preview",  # Updated to the specified GPT-4 model
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": "You are a highly knowledgeable assistant, tasked with refining and formatting content."},
                {"role": "user", "content": f"Refine and format this content: \"{raw_content}\""}
                {"role": "system", "content": "You are an AI who formats provided content into a concise, readable format for web display, ensuring to retain all original details and links."},
                {"role": "user", "content": content}
            ]
        )
        # Extracting the response based on the expected structure for chat completions
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        # Handling exceptions and returning the error message
        return f"An error occurred: {str(e)}"

# Streamlit app layout
st.title('Your Daily Digest and Playlist')
st.title('Your Daily Digest and Playlist Generator')

with st.form("user_input"):
    name = st.text_input("Name")
    vibe = st.text_input("Vibe")
    astro_sign = st.selectbox("Astrological Sign", ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"])
    interests = st.multiselect("Select your interests", ["Positive News", "AI and Tech", "Gossip", "Hip-Hop"])
    vibe = st.text_input("Vibe", help="Describe the vibe for your music playlist.")
    topic = st.text_input("News Topic", help="Enter a topic to get the latest news.")
    submitted = st.form_submit_button("Submit")

if submitted:
    with st.spinner('Fetching your personalized content...'):
        # Fetch horoscope
        horoscope_raw = call_perplexity_api(f"horoscope for {astro_sign}")
        horoscope = refine_content_with_gpt(horoscope_raw)
        # Fetch news
        news_query = f"latest news about {topic} including source links"
        news_content = call_perplexity_api(news_query)

        # Fetch news based on interests
        news_stories = [call_perplexity_api(f"latest news on {topic}") for topic in interests]
        refined_news_stories = [refine_content_with_gpt(story) for story in news_stories]
        # Fetch playlist
        playlist_query = f"music playlist suggestions for a {vibe} vibe including source links"
        playlist_content = call_perplexity_api(playlist_query)

        # Fetch music playlist based on vibe
        playlist_raw = call_perplexity_api(f"music playlist for vibe {vibe}")
        playlist = refine_content_with_gpt(playlist_raw)
        # Optional: Refine content with GPT-4 for readability
        refined_news = refine_content_with_gpt(news_content)
        refined_playlist = refine_content_with_gpt(playlist_content)

    st.success('Here’s what we found for you!')
    st.success('Content fetched successfully!')

    st.subheader('Your Personalized Horoscope')
    st.write(horoscope)
    st.subheader('Latest News')
    st.write(refined_news)

    if refined_news_stories:
        st.subheader('Latest News For You')
        for story in refined_news_stories:
            st.write(story)

    st.subheader('Your Music Playlist Recommendations')
    st.write(playlist)
    st.subheader('Music Playlist Suggestions')
    st.write(refined_playlist) 
