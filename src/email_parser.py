import base64
from bs4 import BeautifulSoup
import json
import logging

def extract_email_content(msg):
    headers = msg['payload']['headers']
    subject = next((header['value'] for header in headers if header['name'] == 'Subject'), '')
    sender = next((header['value'] for header in headers if header['name'] == 'From'), '')
    
    parts = msg['payload'].get('parts', [])
    body = ''
    if parts:
        for part in parts:
            if part['mimeType'] == 'text/plain':
                data = part['body']['data']
                decoded_data = base64.urlsafe_b64decode(data).decode('utf-8')
                body += decoded_data
            elif part['mimeType'] == 'text/html':
                data = part['body']['data']
                decoded_data = base64.urlsafe_b64decode(data).decode('utf-8')
                soup = BeautifulSoup(decoded_data, 'html.parser')
                body += soup.get_text()
    else:
        data = msg['payload']['body'].get('data', '')
        if data:
            decoded_data = base64.urlsafe_b64decode(data).decode('utf-8')
            body += decoded_data
    
    return subject, sender, body

def parse_events(api_response):
    try:
        if isinstance(api_response, dict):
            if 'error' in api_response:
                logging.warning(f"API returned an error: {api_response['error']}")
                return []
            else:
                return [api_response]  # Single event
        elif isinstance(api_response, list):
            return api_response  # List of events
        else:
            logging.error(f"Unexpected API response format: {type(api_response)}")
            return []
    except Exception as e:
        logging.error(f"Error parsing events: {e}")
        return []
