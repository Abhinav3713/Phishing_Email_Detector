# email_fetcher.py
import imaplib
import email
from email.header import decode_header
from config import EMAIL_USER, EMAIL_PASSWORD, IMAP_SERVER, IMAP_PORT

def connect_to_email():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL_USER, EMAIL_PASSWORD)
        mail.select("inbox")  # Select inbox
        return mail
    except Exception as e:
        print(f"Error connecting to email: {e}")
        return None

def fetch_latest_emails(mail, count=10):
    try:
        status, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()[-count:]  # Get last 'count' emails
        emails = []
        
        for email_id in email_ids:
            status, data = mail.fetch(email_id, "(RFC822)")
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8")

                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == "text/plain":
                                body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                                break
                    else:
                        body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
                    
                    emails.append({"subject": subject, "body": body})

        return emails
    except Exception as e:
        print(f"Error fetching emails: {e}")
        return []
