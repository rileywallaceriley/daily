from google_auth_oauthlib.flow import InstalledAppFlow

# Replace these with your client ID and client secret from the Google Cloud Console
CLIENT_ID = 'YOUR_CLIENT_ID.apps.googleusercontent.com'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
# This should match one of the redirect URIs you set in the Google Cloud Console
REDIRECT_URI = 'http://localhost:8080/oauth2callback'
# The YouTube API scope for creating playlists
SCOPES = ['https://www.googleapis.com/auth/youtube']

def main():
    flow = InstalledAppFlow.from_client_config({
        'web': {
            'client_id': '644406040744-a50ea7bn7f8huru39rthr1qvuug04kr0.apps.googleusercontent.com',
            'client_secret': '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',
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'redirect_uris': https://share.streamlit.io/rileywallaceriley/daily/main/create.py,
        }
    }, SCOPES)
    
    # Run the local server to complete the flow
    credentials = flow.run_local_server(port=8080)
    
    # Display the tokens
    print(f"Access Token: {credentials.token}")
    print(f"Refresh Token: {credentials.refresh_token}")

if __name__ == '__main__':
    main()
