import requests
import os
from lead_db import save_lead

def send_webhook(data):
    reference = save_lead(data)
    webhook_url = os.getenv('WEBHOOK_URL')
    if webhook_url and 'error' not in data:
        try:
            data['reference'] = reference
            requests.post(webhook_url, json=data, timeout=5)
        except Exception as e:
            print(f"Webhook error: {e}")