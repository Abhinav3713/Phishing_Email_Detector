# main.py
import time
from email_fetcher import connect_to_email, fetch_latest_emails
from phishing_detector import check_for_phishing
from config import FETCH_INTERVAL

def main():
    mail = connect_to_email()
    if not mail:
        print("Failed to connect to email server.")
        return

    while True:
        print("\nChecking emails...")
        emails = fetch_latest_emails(mail)
        
        for email_data in emails:
            is_phishing, keyword = check_for_phishing(email_data)
            if is_phishing:
                print(f"⚠️ Phishing Alert: Suspicious email detected!")
                print(f"  Subject: {email_data['subject']}")
                print(f"  Triggered Keyword: {keyword}")
            else:
                print(f"✅ Safe Email: {email_data['subject']}")

        print(f"Waiting {FETCH_INTERVAL} seconds before checking again...\n")
        time.sleep(FETCH_INTERVAL)

if __name__ == "__main__":
    main()
