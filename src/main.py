from flask import Flask, redirect, session, url_for, render_template
from gmail_handler import fetch_gmail_emails
from ai_classifier import classify_email
from webhook_sender import send_webhook
from oauth_flow import get_flow, save_token

app = Flask(__name__)
app.secret_key = "super_secret_key"  # Replace with env-secured key in production

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/connect/google")
def connect_google():
    flow = get_flow()
    auth_url, state = flow.authorization_url(access_type="offline", include_granted_scopes="true")
    session["state"] = state
    return redirect(auth_url)

@app.route("/oauth2callback")
def oauth2callback():
    flow = get_flow()
    flow.fetch_token(authorization_response=flask.request.url)
    creds = flow.credentials
    save_token(creds)
    return render_template("success.html")

@app.route("/cron/check")
def cron_check():
    results = []
    emails = fetch_gmail_emails()
    for email in emails:
        ai_result = classify_email(email)
        send_webhook(ai_result)
        results.append(ai_result)
    return {"results": results}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)