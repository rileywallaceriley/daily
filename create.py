def fetch_samples_with_perplexity(song_title):
    """Fetches sample information for a song using Perplexity with the updated model and prompt."""
    headers = {
        'Authorization': f'Bearer {perplexity_api_key}',
        'Content-Type': 'application/json',
    }
    payload = {
        "model": "sonar-medium-online",  # Updated model
        "messages": [
            {
                "role": "system",
                "content": "You are an AI knowledgeable about music samples."
            },
            {
                "role": "user",
                "content": f"songs sampled to make {song_title}"
            }
        ]
    }
    response = requests.post('https://api.perplexity.ai/v1/chat/completions', headers=headers, json=payload)
    if response.status_code == 200:
        sample_info = response.json()['choices'][0]['message']['content']
        if sample_info.strip() and not "I'm not sure" in sample_info:
            st.success('Here are the samples found:')
            for line in sample_info.split('\n'):
                if ' - ' in line:
                    parts = line.split(' - ')
                    if len(parts) >= 2:
                        song_title, artist = parts[0].strip(), parts[1].strip()
                        display_song_with_link(song_title, artist)
                else:
                    # If the line doesn't conform to the expected format, just display the text.
                    # This might be useful for providing additional context or information.
                    st.write(line)
        else:
            st.write("No specific sample information could be retrieved.")
    else:
        st.error(f"Failed to fetch samples: {response.status_code}, {response.text}")