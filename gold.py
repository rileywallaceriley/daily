import streamlit as st
import requests
from datetime import datetime

def fetch_gold_prices(query):
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
        # Assuming the structure of the response; adjust as necessary
        try:
            # You might need to parse the response differently
            # This is just an example
            prices_info = data['choices'][0]['message']['content']
            return {"success": True, "data": prices_info}
        except KeyError:
            return {"success": False, "error": "Failed to parse response data."}
    else:
        return {"success": False, "error": response.text}

# Streamlit UI
st.title('Gold Prices in Canada')

if st.button('Fetch Gold Prices'):
    today_date = datetime.now().strftime('%Y-%m-%d')
    query = f"What are the prices of 10k, 18k, and 24k gold per gram in Canada as of today, {today_date}?"

    result = fetch_gold_prices(query)

    if result["success"]:
        st.success("Data fetched successfully!")
        # Displaying the result in a markdown for better presentation
        st.markdown(f"### Gold Prices on {today_date}")
        st.markdown(result['data'])
    else:
        st.error(f"Error fetching data: {result['error']}")
else:
    st.info('Press the button above to fetch the latest gold prices.')