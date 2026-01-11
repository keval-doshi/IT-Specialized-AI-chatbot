from langchain_google_genai import ChatGoogleGenerativeAI
import os
from langchain_core.output_parsers import StrOutputParser

class LLMFallback:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        self.parser = StrOutputParser()

        if not api_key:
            self.llm = None
        else:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                temperature=0.2
            )

    def get_response(self, user_query: str) -> str:
        if not self.llm:
            return "I’m unable to access advanced help right now. Please contact IT support."

        prompt = f"""
You are an internal IT support assistant.

Give clear, short, step-by-step guidance.
If unsure, suggest contacting IT support.

User issue:
{user_query}
"""

        response = self.llm.invoke(prompt)
        return self.parser.parse(response.content)
