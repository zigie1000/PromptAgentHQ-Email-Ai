import os
import psycopg2
import json
from datetime import datetime

DB_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DB_URL)

def generate_reference():
    today = datetime.utcnow().strftime("%Y%m%d")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM leads_inbox WHERE to_char(created_at, 'YYYYMMDD') = %s", (today,))
    count = cur.fetchone()[0] + 1
    reference = f"LEAD-{today}-{count:04d}"
    cur.close()
    conn.close()
    return reference

def save_lead(data):
    conn = get_connection()
    cur = conn.cursor()
    reference = generate_reference()
    cur.execute("""
        INSERT INTO leads_inbox (
            reference, email_id, sender_name, sender_email,
            subject, summary, urgency, intent, phone,
            listing_ref, preferred_date, raw_payload
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        reference,
        data.get('email_id'),
        data.get('sender', {}).get('name'),
        data.get('sender', {}).get('email'),
        data.get('subject'),
        data.get('summary'),
        data.get('urgency'),
        data.get('intent'),
        data.get('phone'),
        data.get('listing_ref'),
        data.get('preferred_date'),
        json.dumps(data)
    ))
    conn.commit()
    cur.close()
    conn.close()
    return reference