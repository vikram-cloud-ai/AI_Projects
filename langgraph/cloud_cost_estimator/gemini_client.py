import getpass
import os
from dotenv import load_dotenv

load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY") or getpass.getpass("Enter your Google API key: ")

if "LANGSMITH_API_KEY" not in os.environ:
    os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY") or getpass.getpass("Enter your LangSmith API key: ")
if "LANGSMITH_TRACING" not in os.environ:
    os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING") or "true"

from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=1.0,  # Gemini 3.0+ defaults to 1.0
    max_tokens=None,
    timeout=None,
    max_retries=2,
    thinking_level="minimal",  # Gemini 3.0+ defaults to "medium"
)

messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]
ai_msg = model.invoke(messages)
print(ai_msg.content)
print("\nUsage Metadata:")
print(ai_msg.usage_metadata)
