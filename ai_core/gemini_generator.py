import os
import logging
from typing import Optional
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

LEGAL_DISCLAIMER = (
    "\n\n---\nDISCLAIMER: This document is AI-generated for informational purposes only. "
    "It should be reviewed by a qualified legal professional before use."
)


class GeminiGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

    async def generate(
        self,
        document_type: str,
        parties: str,
        terms_conditions: str,
        effective_date: str
    ) -> str:
        prompt = self._build_prompt(document_type, parties, terms_conditions, effective_date)

        try:
            response = self.model.generate_content(prompt)
            document_text = response.text.strip()
            return document_text + LEGAL_DISCLAIMER
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise ValueError("AI service temporarily unavailable. Please try again.")

    def _build_prompt(
        self,
        document_type: str,
        parties: str,
        terms_conditions: str,
        effective_date: str
    ) -> str:
        return f"""Generate a professional {document_type} with the following details:

PARTIES INVOLVED:
{parties}

TERMS AND CONDITIONS:
{terms_conditions}

EFFECTIVE DATE:
{effective_date}

Requirements:
1. Use formal legal language appropriate for a {document_type}
2. Include all standard sections relevant to this document type
3. Structure the document with clear headings and numbered clauses
4. Include signature blocks for all parties
5. Add a governing law clause
6. Ensure the document is comprehensive and professionally formatted

Output the complete document text only, without any additional commentary."""
