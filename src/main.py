from gmail_api import get_service, fetch_emails
from email_parser import extract_email_content, parse_events
from event_extractor import process_email
from report_generator import generate_report
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Authenticate and create Gmail API service
    service = get_service()
    
    # Fetch emails from the past week
    messages = fetch_emails(service, query='newer_than:7d', max_results=3)
    logging.info(f"Fetched {len(messages)} emails")
    
    events_by_email = {}
    for msg in messages:
        # Extract email components
        subject, sender, body = extract_email_content(msg)
        logging.info(f"Processing email: {subject}")
        
        # Process the email using the event extractor
        result = process_email(body)
        
        # Parse the events from the API response
        parsed_events = parse_events(result)
        
        if parsed_events:
            # Store the extracted events
            events_by_email[subject] = parsed_events
            logging.info(f"Extracted {len(parsed_events)} event(s) from email: {subject}")
        else:
            logging.info(f"No events extracted from email: {subject}")
    
    if events_by_email:
        # Generate the report
        generate_report(events_by_email)
        logging.info(f"Generated report with events from {len(events_by_email)} emails")
    else:
        logging.warning("No events were extracted from any emails. Report not generated.")

if __name__ == '__main__':
    main()
