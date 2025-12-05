# openai_agent.py (updated)
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

class OpenAIAgent:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def get_response(self, user_input: str, tone: str, language: str, memory: list = []):
        try:
            system_prompt = {
                "role": "system",
                "content": f"You are DEVA, a multilingual, empathetic AI mentor. Reply in {language}, using a {tone} tone."
            }

            messages = [system_prompt] + memory + [{"role": "user", "content": user_input}]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=600
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return "Sorry, I had trouble accessing my memory. Please try again later."
