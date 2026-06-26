import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found in .env file")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


def generate_itinerary(source, destination, start_date, end_date, no_of_day):
    prompt = (
        f"Generate a detailed {no_of_day}-day travel itinerary from {source} "
        f"to {destination} between {start_date} and {end_date}. "
        f"Include places to visit, activities, food suggestions, "
        f"and an estimated budget in INR."
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ ACTIVE & SUPPORTED
            messages=[
                {"role": "system", "content": "You are an expert travel planner."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=900
        )

        return response.choices[0].message.content

    except Exception as e:
        print("❌ Groq API Error:", type(e).__name__, str(e))
        return "Unable to generate itinerary right now. Please try again later."
