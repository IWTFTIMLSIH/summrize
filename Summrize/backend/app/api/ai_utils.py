import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_document(text: str) -> str:
    prompt = f"""
You are an Alberta-based condominium document reviewer. The following text is extracted from a condominium document.

Your task:
- Summarize the contents in plain English.
- Highlight any red flags (lawsuits, low reserves, special assessments, restrictive rules).
- Mention any important bylaws, financial or legal issues.

Document:
{text}

Provide the summary below:
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=600
        )
        summary = response["choices"][0]["message"]["content"]
        return summary
    except Exception as e:
        return f"Error during AI processing: {e}"