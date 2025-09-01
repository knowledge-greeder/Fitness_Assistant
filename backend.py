import os
from dotenv import load_dotenv
import google.generativeai as genai

# ---------------- Backend Setup ----------------
# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")


def format_prompt(user_input, user_profile=""):
    """Format user query into a structured prompt for better answers."""
    return f"""
    You are a safe, helpful health assistant.
    User Profile: {user_profile}

    Rules:
    - Do NOT provide diagnosis or prescriptions.
    - Give general health & wellness advice only.
    - Encourage consulting a doctor if necessary.

    User: {user_input}
    Assistant:
    """


def get_chatbot_response(user_input, user_profile=""):
    """Send formatted query to Google AI Studio and return model response."""
    prompt = format_prompt(user_input, user_profile)
    response = model.generate_content(prompt)
    return response.text


def calculate_bmi(weight, height):
    """Calculate BMI from weight (kg) and height (cm)."""
    return weight / ((height / 100) ** 2)


def calculate_maintenance_calories(weight, activity_level):
    """Estimate maintenance calories based on activity level."""
    activity_map = {
        "Sedentary": 1.2,
        "Light": 1.375,
        "Moderate": 1.55,
        "Active": 1.8,
    }
    factor = activity_map.get(activity_level, 1.2)
    return weight * 22 * factor
