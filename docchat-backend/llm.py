# llm.py
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_answer_with_context(query, context_chunks):
    context = "\n\n".join(context_chunks)
    prompt = f"""
You are DocChat, an intelligent assistant. Use the context below to answer the question.

Context:
{context}

Question: {query}
Answer:
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful AI documentation assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=500
    )
    return response['choices'][0]['message']['content'].strip()