import sys
import os
import unittest
from unittest.mock import MagicMock

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src import email_parser
from src import gmail_api

class TestEmailParser(unittest.TestCase):

    def setUp(self):
        self.gmail_service = gmail_api.get_service()

    def test_extract_email_content(self):
        # Fetch a real email to test with
        query = "is:unread"
        messages = gmail_api.fetch_emails(self.gmail_service, query)
        
        if not messages:
            self.skipTest("No unread messages available for testing")

        # Get the full message details
        msg = self.gmail_service.users().messages().get(userId='me', id=messages[0]['id']).execute()

        # Test the extract_email_content function
        subject, sender, body = email_parser.extract_email_content(msg)

        # Assert that we got some content
        self.assertIsNotNone(subject)
        self.assertIsNotNone(sender)
        self.assertIsNotNone(body)

        # Print out the extracted content for manual verification
        print(f"Subject: {subject}")
        print(f"Sender: {sender}")
        print(f"Body (first 100 characters): {body[:100]}...")

    def test_extract_email_content_mock(self):
        # Create a mock message
        mock_msg = {
            'payload': {
                'headers': [
                    {'name': 'Subject', 'value': 'Test Subject'},
                    {'name': 'From', 'value': 'test@example.com'}
                ],
                'body': {
                    'data': 'VGhpcyBpcyBhIHRlc3QgYm9keQ==' # "This is a test body" in base64
                }
            }
        }

        # Test the extract_email_content function with the mock message
        subject, sender, body = email_parser.extract_email_content(mock_msg)

        self.assertEqual(subject, 'Test Subject')
        self.assertEqual(sender, 'test@example.com')
        self.assertEqual(body, 'This is a test body')

if __name__ == '__main__':
    unittest.main()