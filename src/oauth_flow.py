import os
import json
import flask
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:5000/oauth2callback")

def get_flow():
    return Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

def save_token(creds):
    with open("token.json", "w") as token_file:
        token_file.write(creds.to_json())

def load_token():
    if os.path.exists("token.json"):
        return Credentials.from_authorized_user_file("token.json", SCOPES)
    return None