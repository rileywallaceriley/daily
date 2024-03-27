from google_auth_oauthlib.flow import Flow
import streamlit as st

# Replace these with your client ID and client secret from the Google Cloud Console
CLIENT_ID = '644406040744-a50ea7bn7f8huru39rthr1qvuug04kr0.apps.googleusercontent.com'
CLIENT_SECRET = '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'
# The YouTube API scope for creating playlists
SCOPES = ['https://www.googleapis.com/auth/youtube']

# This should match one of the redirect URIs you set in the Google Cloud Console, adapted for manual copying of the code
REDIRECT_URI = 'https://share.streamlit.io/rileywallaceriley/daily/main/create.py'

def main():
    if 'flow' not in st.session_state:
        st.session_state['flow'] = Flow.from_client_config(
            client_config={
                'web': {
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                    'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                    'token_uri': 'https://oauth2.googleapis.com/token',
                    'redirect_uris': [REDIRECT_URI],
                }
            },
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )

    if 'auth_url' not in st.session_state:
        auth_url, _ = st.session_state['flow'].authorization_url(prompt='consent', access_type='offline')
        st.session_state['auth_url'] = auth_url
        st.markdown(f'Please go to this URL and authorize access: [Authorization Link]({auth_url})')

    authorization_response = st.text_input('Paste the full authorization response URL here:')
    
    if authorization_response:
        st.session_state['flow'].fetch_token(authorization_response=authorization_response)
        credentials = st.session_state['flow'].credentials
        
        # Display tokens for debugging; in a real app, you'd use these credentials to make API calls
        st.text(f"Access Token: {credentials.token}")
        st.text(f"Refresh Token: {credentials.refresh_token}")

if __name__ == '__main__':
    main()
