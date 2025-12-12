# newsportal_backEnd/news/llm_news.py

import os
import openai
from openai import OpenAI

openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_news(title, category=None, reporter=None, length=300):
    """
    Generate a news article using LLM
    :param title: News headline
    :param category: Category name (optional)
    :param reporter: Reporter name (optional)
    :param length: Number of words (approx)
    :return: Generated content
    """
    prompt = f"Write a professional news article in Hindi for the headline: '{title}'"
    if category:
        prompt += f" under the category '{category}'"
    if reporter:
        prompt += f" attributed to reporter '{reporter}'"
    prompt += f". Keep it around {length} words."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",   # or "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are a professional news writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=600,
    )

    content = response['choices'][0]['message']['content']
    return content.strip()
