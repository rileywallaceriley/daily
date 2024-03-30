import openai
import streamlit as st

# Assuming your OpenAI API key is correctly set in Streamlit's secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def format_search_results(search_results):
    """Formats the search results for vinyl records using the GPT-4 Chat model."""
    try:
        formatted_response = openai.ChatCompletion.create(
            model="gpt-4-0125-preview",  # Make sure this is the correct model identifier
            messages=[
                {"role": "system", "content": "You are an AI trained to organize and present search results for vinyl records in a concise, easy-to-read format. Include relevant details such as the title, artist, release date, and a direct link."},
                {"role": "user", "content": f"Search results: {search_results}"}
            ]
        )
        return formatted_response.choices[0].message['content']
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return ""

# Example usage within Streamlit
st.title('Vinyl Hunter')

# This part is where you'd integrate the search functionality
# For demonstration, we're using placeholder search results
placeholder_search_results = "Here are some placeholder search results about vinyl records."
if st.button('Format Search Results'):
    results = format_search_results(placeholder_search_results)
    st.write('Formatted Search Results:')
    st.write(results)