import streamlit as st
import requests
from datetime import datetime

# Function to fetch data from Perplexity
def fetch_gold_price(query):
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

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        # Temporarily print the entire response to inspect its structure
        st.write(data)
        return {"success": True, "data": data}
    else:
        return {"success": False, "error": response.text}

# Streamlit UI setup to inspect the response
st.title('Gold Price in Canada')
today_date = datetime.now().strftime('%Y-%m-%d')
query = f"What is the price of gold per gram in Canada as of today, {today_date}?"
fetch_gold_price(query)