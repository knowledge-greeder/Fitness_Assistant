import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# ---------------- Backend Setup ----------------

# Try to load API key from .env (local dev)
if os.path.exists(".env"):
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
else:
    # Fallback: use Streamlit secrets in production
    api_key = st.secrets.get("GOOGLE_API_KEY")

# Configure Gemini model
if not api_key:
    raise ValueError("❌ GOOGLE_API_KEY is missing. Please set it in .env (local) or st.secrets (production).")

genai.configure(api_key=api_key)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")


# ---------------- Utility Functions ----------------
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


def calculate_bmi(weight, height_cm):
    """Calculate BMI from weight (kg) and height (cm)."""
    return weight / ((height_cm / 100) ** 2)


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
