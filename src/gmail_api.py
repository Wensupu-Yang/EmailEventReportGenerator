import os.path
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

print("gmail_api.py is being imported")

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_service():
    creds = None
    token_path = 'credentials/token.json'
    creds_path = 'credentials/client_secret_493109570724-i6jp6g0q98tmc2k7n2opufro32na1fi7.apps.googleusercontent.com.json'

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    # If there are no valid credentials, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for future runs
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


def fetch_emails(service, query='', max_results=None):
    try:
        # Fetch messages
        results = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
        messages = results.get('messages', [])

        # Fetch full message for each email
        return [service.users().messages().get(userId='me', id=msg['id']).execute() for msg in messages]
    except Exception as error:
        print(f'An error occurred: {error}')
        return []


def get_emails():
    # ... (implement the logic to fetch emails)
    # This function should return a list of email messages

    # Example implementation:
    creds = None
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API to fetch emails
    results = service.users().messages().list(userId='me', maxResults=10).execute()
    messages = results.get('messages', [])

    return messages

# Make sure to export the function
__all__ = ['get_emails']
