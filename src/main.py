from gmail_api import get_service, fetch_emails
from email_parser import extract_email_content, parse_events
from event_extractor import process_email
from calendar_generator import generate_calendar
from report_generator import generate_report
from datetime import datetime
import logging
import json
import time
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_events_log(events_by_email):
    # Create timestamp for the filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'logs/events_log_{timestamp}.json'
    
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    # Save the events dictionary to a JSON file
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(events_by_email, f, indent=2, ensure_ascii=False)
        logging.info(f"Events log saved to {filename}")
    except Exception as e:
        logging.error(f"Failed to save events log: {e}")

def main():
    # Authenticate and create Gmail API service
    service = get_service()
    
    # Fetch emails from the past week
    messages = fetch_emails(service, query='newer_than:7d', max_results=100)  # Increased to 100
    logging.info(f"Fetched {len(messages)} emails")
    
    events_by_email = {}
    for i, msg in enumerate(messages):
        # Add rate limiting
        if i > 0 and i % 3 == 0:  # Add delay every 3 requests
            time.sleep(1)  # 1 second delay
            
        # Extract email components
        subject, sender, body = extract_email_content(msg)
        logging.info(f"Processing email {i+1}/{len(messages)}: {subject}")
        logging.info(f"Email body preview: {body[:100]}...")  # Log a preview of the email body
        
        # Process the email using the event extractor
        result = process_email(body)
        
        # Parse the events from the API response
        parsed_events = parse_events(result)
        
        if parsed_events:
            # Store the extracted events
            events_by_email[subject] = parsed_events
            logging.info(f"Extracted {len(parsed_events)} event(s) from email: {subject}")
            for event in parsed_events:
                logging.info(f"Event details: {json.dumps(event, indent=2)}")
        else:
            logging.info(f"No events extracted from email: {subject}")
    
    if events_by_email:
        # Save events log before generating calendar and report
        save_events_log(events_by_email)
        
        # Generate the calendar
        generate_calendar(events_by_email)
        # Generate the report
        generate_report(events_by_email)
        logging.info(f"Generated calendar and report with events from {len(events_by_email)} emails")
    else:
        logging.warning("No events were extracted from any emails. Calendar and report not generated.")

if __name__ == '__main__':
    main()
