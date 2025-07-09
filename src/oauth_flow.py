import os
from google_auth_oauthlib.flow import Flow

def get_flow():
    return Flow.from_client_config(
        {
            "web": {
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [os.getenv("REDIRECT_URI")]
            }
        },
        scopes=["https://www.googleapis.com/auth/gmail.readonly"],
        redirect_uri=os.getenv("REDIRECT_URI")
    )

def save_token(creds):
    with open("token.json", "w") as token_file:
        token_file.write(creds.to_json())

def load_token():
    if os.path.exists("token.json"):
        from google.oauth2.credentials import Credentials
        return Credentials.from_authorized_user_file("token.json")
    return None
