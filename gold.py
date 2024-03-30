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
        # Example parsing logic, adjust based on actual response structure
        try:
            # Extract and return the gold price and date from the response
            gold_price_info = data['data']['content']  # Adjust based on actual key paths
            return {"success": True, "data": gold_price_info}
        except KeyError:
            return {"success": False, "error": "Failed to parse response data."}
    else:
        return {"success": False, "error": response.text}

# Streamlit UI
st.title('Gold Price in Canada')

# Today's date for the query
today_date = datetime.now().strftime('%Y-%m-%d')
query = f"What is the price of gold per gram in Canada as of today, {today_date}?"

# Fetching gold price data
result = fetch_gold_price(query)

if result["success"]:
    # Displaying the result
    st.success("Data fetched successfully!")
    
    # Aesthetically pleasing presentation
    st.markdown(f"### Gold Price on {today_date}")
    st.markdown(f"**Price per gram:** {result['data']}")
    
    # Example of adding visual elements
    st.metric(label="Gold Price (per gram)", value=result['data'])
else:
    st.error(f"Error fetching data: {result['error']}")