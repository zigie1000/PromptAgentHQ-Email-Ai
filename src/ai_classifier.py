import openai
import os
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")

def classify_email(email):
    prompt = f"""Classify this email and extract structured information:
Subject: {email['subject']}
Body: {email['body']}

Return JSON with:
- urgency (urgent/actionable/fyi)
- type (inquiry/spam/update)
- name
- phone
- listing_ref
- preferred_date
- summary (1-sentence)
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        extracted = eval(response['choices'][0]['message']['content'])

        return {
            "email_id": email.get("id", "unknown"),
            "timestamp": datetime.utcnow().isoformat(),
            "sender": {
                "name": extracted.get("name", "Unknown"),
                "email": email.get("from", "unknown@example.com")
            },
            "subject": email['subject'],
            "summary": extracted.get("summary"),
            "urgency": extracted.get("urgency"),
            "intent": extracted.get("type"),
            "phone": extracted.get("phone"),
            "listing_ref": extracted.get("listing_ref"),
            "preferred_date": extracted.get("preferred_date")
        }
    except Exception as e:
        return {"error": str(e), "subject": email['subject']}