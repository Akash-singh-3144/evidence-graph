import logging
from google import genai
from app.config.settings import settings
import json

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = settings.GEMINI_MODEL

    async def generate_response(self, prompt: str, schema=None):
        try:
            config = {"response_mime_type": "application/json"} if schema else {}
            # Simplified genai SDK stub usage
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config
            )
            text = response.text
            if schema:
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    # Basic fallback logic for dirty markdown json responses
                    clean = text.replace("```json", "").replace("```", "").strip()
                    return json.loads(clean)
            return text
        except Exception as e:
            logger.error(f"Gemini API Error: {str(e)}")
            raise e
