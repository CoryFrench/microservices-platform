import requests
import logging

# Fetch Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def send_email(api_key, subject, message_text, from_email, to_email):
    url = "https://mandrillapp.com/api/1.0/messages/send.json"
    to_list = [{"email": to_email, "type": "to"}]

    logger.info(f"To list: {to_list}")

    data = {
        "key": api_key,
        "message": {
            "from_email": from_email,
            "to": to_list,
            "subject": subject,
            "text": message_text
        }
    }
    response = requests.post(url, json=data)
    logger.info(f"Email response: {response.json()}")
    return response.json()