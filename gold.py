import streamlit as st
import requests

def fetch_data_from_perplexity(query):
    url = 'https://api.perplexity.ai/chat/completions'
    headers = {
        'Authorization': f'Bearer {st.secrets["PERPLEXITY_API_KEY"]}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    payload = {
        "model": "sonar-medium-online",
        "messages": [{"role": "user", "content": query}]
    }

    with st.spinner('Fetching...'):
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": response.text}

# Streamlit UI
st.title('Current Prices Fetcher')

query = "What is the current price of both silver and gold per gram as of today’s date in CAD?"

result = fetch_data_from_perplexity(query)

if result["success"]:
    st.success("Data fetched successfully!")
    st.json(result["data"])  # Displaying the fetched data in JSON format on the app
else:
    st.error(f"Error fetching data: {result['error']}")