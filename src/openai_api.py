# src/openai_api.py

from dotenv import load_dotenv
import os
from openai import OpenAI
import json
import logging

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def get_completion(prompt, system_message):
    """
    Generic function to get a completion from the OpenAI API.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip()

def get_json_completion(prompt, system_message):
    """
    Get a completion from the OpenAI API and parse it as JSON.
    """
    response = get_completion(prompt, system_message)
    logging.info(f"Raw API response: {response}")
    try:
        # Remove markdown code block formatting if present
        cleaned_response = response.replace('```json', '').replace('```', '').strip()
        json_response = json.loads(cleaned_response)
        logging.info(f"Parsed JSON response: {json_response}")
        return json_response
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON: {e}")
        logging.error(f"Response that failed to parse: {response}")
        return {"error": "Failed to parse JSON response"}