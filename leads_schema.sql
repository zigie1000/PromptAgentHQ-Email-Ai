CREATE TABLE IF NOT EXISTS leads_inbox (
    lead_id SERIAL PRIMARY KEY,
    reference VARCHAR(30) UNIQUE NOT NULL,
    email_id VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sender_name VARCHAR(100),
    sender_email VARCHAR(100),
    subject TEXT,
    summary TEXT,
    urgency VARCHAR(20),
    intent VARCHAR(50),
    phone VARCHAR(30),
    listing_ref VARCHAR(100),
    preferred_date DATE,
    raw_payload JSONB,
    is_followed_up BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);