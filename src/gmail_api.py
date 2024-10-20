import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
TOKEN_PATH = 'credentials/token.pickle'
CREDS_PATH = 'credentials/client_secret_493109570724-i6jp6g0q98tmc2k7n2opufro32na1fi7.apps.googleusercontent.com.json'

def get_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                logging.error(f"Error refreshing credentials: {e}")
                if os.path.exists(TOKEN_PATH):
                    os.remove(TOKEN_PATH)
                return get_service()  # Retry authentication
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        logging.error(f"Error building Gmail service: {e}")
        raise

def fetch_emails(service, query='', max_results=5):
    try:
        results = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
        messages = results.get('messages', [])
        return [service.users().messages().get(userId='me', id=msg['id']).execute() for msg in messages]
    except Exception as error:
        logging.error(f'An error occurred while fetching emails: {error}')
        return []

# Export the necessary functions
__all__ = ['get_service', 'fetch_emails']
