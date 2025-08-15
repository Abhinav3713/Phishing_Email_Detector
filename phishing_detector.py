# phishing_detector.py
PHISHING_KEYWORDS = ["urgent", "verify", "account", "suspicious", "password", "click here", "login", "security alert"]

def check_for_phishing(email_data):
    subject = email_data["subject"].lower()
    body = email_data["body"].lower()

    for keyword in PHISHING_KEYWORDS:
        if keyword in subject or keyword in body:
            return True, keyword

    return False, None
