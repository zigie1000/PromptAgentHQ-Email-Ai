import json
import os
from google.oauth2.credentials import Credentials

def save_token_to_file(creds, path="token.json"):
    with open(path, "w") as f:
        f.write(creds.to_json())

def load_token_from_file(path="token.json"):
    if os.path.exists(path):
        return Credentials.from_authorized_user_file(path)
    return None