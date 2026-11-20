
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def generate_health_remarks(glucose, haemoglobin, cholesterol):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "AI remarks unavailable: Gemini API key is missing."

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
You are an AI health information assistant.

Review these blood test values:
Glucose: {glucose}
Haemoglobin: {haemoglobin}
Cholesterol: {cholesterol}

Instructions:
- Do not assume measurement units.
- Do not assume whether glucose was fasting or random.
- Explain that interpretation depends on units and lab reference ranges.
- Do not diagnose any disease.
- Give cautious, understandable health information.
- Recommend professional medical review.
- Include a medical disclaimer.

Format:
1. Blood Test Value Explanation
2. Potential Health Concerns
3. Recommendations
4. Disclaimer
"""

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text or "AI returned an empty response."

    except Exception as error:
        print("Gemini API Error:", error)
        return f"AI service temporarily unavailable: {error}"
