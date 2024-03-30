import streamlit as st
import openai

# Set your OpenAI API key from Streamlit's secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def format_search_results_with_gpt4(search_query):
    """Formats the search results for vinyl records using the GPT-4 Chat model based on a user's search query."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-0125-preview",  # Ensure this model is correct and available
            messages=[
                {"role": "system", "content": "You are an AI trained to find and present information about vinyl records based on a search query. Provide details such as the title, artist, release date, and a direct link if available."},
                {"role": "user", "content": f"Search for: {search_query}"}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return ""

st.title('Vinyl Hunter')

# User input for the search query
search_query = st.text_input('Enter the artist or album you are searching for:')

if search_query:
    # Call the function to format search results with GPT-4
    formatted_results = format_search_results_with_gpt4(search_query)
    
    if formatted_results:
        # Display the formatted results
        st.subheader('Search Results')
        st.write(formatted_results)
    else:
        st.write("No results found or there was an error processing your request.")