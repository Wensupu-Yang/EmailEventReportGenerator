# src/event_extractor.py

from openai_api import get_completion, get_json_completion
import logging

def check_event_relevance(email_body):
    prompt = f"""
    Determine if the following email contains information about an upcoming event.
    Respond with 'Yes' if it does, or 'No' if it doesn't.

    Email:
    {email_body}

    Response (Yes/No):
    """
    system_message = "You are a helpful assistant that determines if an email contains event information."
    
    response = get_completion(prompt, system_message)
    return response.lower() == 'yes'

def extract_event_details(email_body):
    prompt = f"""
    Extract the following details from the text below:
    - Event Name
    - Date
    - Time
    - Venue/Location
    - Registration Link (if any)

    Text:
    {email_body}

    Provide the answer in JSON format.
    """
    system_message = "You are a helpful assistant that extracts event details from email bodies."
    
    return get_json_completion(prompt, system_message)

def process_email(body):
    system_message = """
    You are an AI assistant tasked with extracting event information from email content.
    Your job is to identify key details about events mentioned in the email and return them in a structured format.
    If no event information is found, explicitly state that no event was found.
    """

    prompt = f"""
    Extract event information from the following email content:

    {body}

    Return the information in the following JSON format:
    {{
        "title": "Event title",
        "date": "Event date",
        "time": "Event time",
        "location": "Event location",
        "description": "Brief description of the event"
    }}

    If no event information is found, return:
    {{
        "error": "No event information found in the email content."
    }}
    """

    logging.info(f"Sending prompt to OpenAI API: {prompt[:100]}...")
    result = get_json_completion(prompt, system_message)
    
    logging.info(f"Raw API Response: {result}")
    
    return result  # Return the raw result, parsing will be done in email_parser.py