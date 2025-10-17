"""
Hugging Face Inference API integration for ConversAI MVP.
Handles conversation generation by calling the Llama-3-8B-Instruct model API.
Author: ConversAI MVP
Run: python -c "from model import get_response; print(get_response('Hello', 'test_session'))"
"""

import os
import requests
import logging
import time
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv(override=True) # Add override=True to ensure .env values take precedence

# Hugging Face Inference API configuration
# This is the official endpoint for the Llama 3.1 8B Instruct model.
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.1-8B-Instruct"
# --- Sanity Check URL ---
# If Llama-3.1 still fails, comment the line above and uncomment the one below to test with a public model.
# API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
HF_TOKEN = os.getenv("HF_TOKEN")

# --- Diagnostic Check ---
# Log the loaded token to verify it's correct. We only log the start and end to keep it secure.
if HF_TOKEN:
    logger.info(f"Loaded HF_TOKEN successfully. Starts with '{HF_TOKEN[:5]}' and ends with '{HF_TOKEN[-4:]}'.")

MAX_RETRIES = 3
RETRY_WAIT_SECONDS = 10


def get_response(user_input: str, session_id: str) -> str:
    """
    Generate a response by calling the Hugging Face Inference API.
    
    Args:
        user_input: The user's message
        session_id: Unique identifier for the conversation session

    Returns:
        str: The bot's response
    """
    if not HF_TOKEN:
        logger.error("HF_TOKEN environment variable not set.")
        return "Sorry, the AI service is not configured correctly. Please contact the administrator."

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": user_input,
        "parameters": {
            "return_full_text": False,
            "max_new_tokens": 250
        }
    }

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            
            # If the model is loading, Hugging Face returns a 503 error.
            # We should wait and retry.
            if response.status_code == 503:
                wait_time = response.json().get("estimated_time", RETRY_WAIT_SECONDS)
                logger.info(f"Model is loading, retrying in {wait_time:.2f} seconds... (Attempt {attempt + 1}/{MAX_RETRIES})")
                time.sleep(wait_time)
                continue

            response.raise_for_status()  # Raise an exception for other bad status codes (4xx or 5xx)

            result = response.json()
            
            if result and isinstance(result, list) and 'generated_text' in result[0]:
                bot_response = result[0]['generated_text'].strip()
                return bot_response
            else:
                logger.error(f"Unexpected API response format: {result}")
                return "I'm sorry, I received an unusual response from the AI. Please try again."

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed on attempt {attempt + 1}: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(2) # Wait a couple of seconds before the next retry for general network issues
            else:
                return "I'm sorry, I'm having trouble connecting to the AI service. Please try again in a moment."
        except Exception as e:
            logger.error(f"Error processing API response: {e}")
            return "I'm sorry, an unexpected error occurred. Please try again."
    
    return "Sorry, the AI model is currently unavailable after multiple attempts. Please try again later."

if __name__ == "__main__":
    # Test the model
    print("Testing ConversAI model...")
    response = get_response("Hello, how are you?", "test_session")
    print(f"Bot: {response}")

    response2 = get_response("What's your name?", "test_session")
    print(f"Bot: {response2}")
