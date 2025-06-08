import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
default_model = os.getenv("OPENAI_MODEL", "gpt-4o")

def generate_response_from_context(user_query, context_text, model=None):
    model = model or default_model
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "Answer the query based on the provided context."},
            {"role": "user", "content": f"Context:\n{context_text}\n\nQuery:\n{user_query}"}
        ],
        temperature=0.3,
        max_tokens=500
    )
    return response['choices'][0]['message']['content']