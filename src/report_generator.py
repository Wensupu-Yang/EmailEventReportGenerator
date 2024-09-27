import os

def generate_report(events_by_email):
    output_path = os.path.join('data', 'event_report.md')
    os.makedirs('data', exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write("# Event Report\n\n")
        for email_subject, events in events_by_email.items():
            f.write(f"## Email: {email_subject}\n\n")
            if isinstance(events, list):
                for event in events:
                    write_event(f, event)
            elif isinstance(events, dict):
                write_event(f, events)
            else:
                f.write(f"Error: Unexpected event format for email '{email_subject}'\n\n")
            f.write("---\n\n")  # Add a separator between emails
    
    print(f"Report generated at {output_path}")

def write_event(f, event):
    f.write(f"### {event.get('title', 'Untitled Event')}\n\n")
    f.write(f"- **Date**: {event.get('date', 'N/A')}\n")
    f.write(f"- **Time**: {event.get('time', 'N/A')}\n")
    f.write(f"- **Location**: {event.get('location', 'N/A')}\n")
    f.write(f"- **Description**: {event.get('description', 'N/A')}\n\n")
