import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import src.gmail_api as gmail_api

print("Contents of gmail_api module:", dir(gmail_api))

def main():
    # Get the Gmail service
    service = gmail_api.get_service()
    
    # Test fetching emails
    query = "is:unread"  # This will fetch unread emails
    messages = gmail_api.fetch_emails(service, query)
    
    print(f"Found {len(messages)} unread messages.")
    
    # Print the first few message IDs
    for message in messages[:5]:
        print(f"Message ID: {message['id']}")

if __name__ == "__main__":
    main()