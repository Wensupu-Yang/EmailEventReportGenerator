from ics import Calendar, Event
from datetime import datetime, date
import os
import logging
import re
from dateutil import parser as date_parser

def generate_calendar(events_by_email):
    calendar = Calendar()
    
    for email_subject, events in events_by_email.items():
        if isinstance(events, list):
            # Multiple events from one email
            for event_data in events:
                event = create_calendar_event(event_data, email_subject)
                if event:
                    calendar.events.add(event)
        elif isinstance(events, dict):
            # Single event from email
            event = create_calendar_event(events, email_subject)
            if event:
                calendar.events.add(event)
        else:
            logging.warning(f"Error: Unexpected event format for email '{email_subject}'")
    
    # Save the calendar to a file
    output_path = os.path.join('data', 'events_calendar.ics')
    os.makedirs('data', exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write(str(calendar))
    
    logging.info(f"Calendar generated at {output_path}")
    logging.info(f"Number of events in calendar: {len(calendar.events)}")

def create_calendar_event(event_data, email_subject):
    event = Event()
    event.name = event_data.get('title', 'Untitled Event')
    
    date_str = event_data.get('date', '')
    time_str = event_data.get('time', '')

    if date_str:
        try:
            event_date = parse_date(date_str)
            if time_str and time_str.lower() not in ['not specified', 'tbd', 'all day']:
                # Both date and time available
                event_time = parse_time(time_str)
                event.begin = datetime.combine(event_date, event_time)
            else:
                # Only date available, make it an all-day event
                event.begin = event_date
                event.make_all_day()
            logging.info(f"Successfully created event: {event.name} on {event.begin}")
        except ValueError as e:
            logging.warning(f"Error parsing date/time for event: {event.name}. Error: {str(e)}")
            logging.warning(f"Date string: '{date_str}', Time string: '{time_str}'")
            return None
    else:
        # No date information available, skip creating event
        logging.warning(f"No date information available for event: {event.name}. Skipping event creation.")
        return None
    
    event.location = event_data.get('location', '')
    event.description = f"From email: {email_subject}\n\n{event_data.get('description', '')}"
    
    return event

def parse_date(date_str):
    try:
        # Use dateutil parser for flexible date parsing
        parsed_date = date_parser.parse(date_str, fuzzy=True)
        return parsed_date.date()
    except ValueError:
        # Handle special cases
        if '-' in date_str:
            # For date ranges, use the start date
            start_date = date_str.split('-')[0].strip()
            return parse_date(start_date)
        elif 'open until' in date_str.lower():
            # For "open until" dates, use the end date
            end_date = date_str.split('open until')[-1].strip()
            return parse_date(end_date)
        else:
            raise ValueError(f"Unable to parse date: {date_str}")

def parse_time(time_str):
    try:
        # Use dateutil parser for flexible time parsing
        parsed_time = date_parser.parse(time_str, fuzzy=True)
        return parsed_time.time()
    except ValueError:
        # Handle special cases
        if '-' in time_str:
            # For time ranges, use the start time
            start_time = time_str.split('-')[0].strip()
            return parse_time(start_time)
        else:
            raise ValueError(f"Unable to parse time: {time_str}")

# If you want to run this script independently
if __name__ == '__main__':
    # Example usage
    events_by_email = {
        "Team Meeting": {
            "title": "Weekly Team Meeting",
            "date": "2023-05-15",
            "time": "14:00",
            "location": "Conference Room A",
            "description": "Discuss project progress and upcoming deadlines."
        },
        "Conference Invitation": [
            {
                "title": "Tech Conference 2023",
                "date": "10 June 2023",
                "time": "09:00 AM",
                "location": "Convention Center",
                "description": "Annual technology conference with keynote speakers and workshops."
            },
            {
                "title": "Networking Event",
                "date": "11-12 June",
                "location": "Hotel Lounge",
                "description": "Evening networking event for conference attendees."
            },
            {
                "title": "Incomplete Event",
                "location": "Unknown",
                "description": "This event has no date or time information."
            }
        ]
    }
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    generate_calendar(events_by_email)