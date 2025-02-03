import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
DEFAULT_CACHE_DIR = os.getenv('CACHE_DIR')


class ArticleSummaryRequest(BaseModel):
    """
    Request model for summarizing an article.
    """
    title: str
    summarized_text: str
    tags: list[str]  # Removed the default value here


def generate_summary(article_text: str) -> ArticleSummaryRequest:
    """
    Generate a summary for the given article text using ChatGPT.

    Args:
        article_text (str): The text of the article to summarize.
        max_tokens (int): The maximum number of tokens for the summary.

    Returns:
        str: The generated summary, or an empty string if an error occurs.
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant that summarizes text."},
        {"role": "user", "content": f"Please summarize the following article text in a concise and clear manner extracting the main take ways from it, also generate in maximun 3 tags relating to the content of the text:\n\n{article_text}"}
    ]

    try:
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini-2024-07-18",  # Use your preferred ChatGPT model
            messages=messages,
            temperature=0.3,
            n=1,
            response_format=ArticleSummaryRequest
        )
        summary = response.choices[0].message.parsed
        return summary
    except Exception as e:
        print(f"Error generating summary: {e}")
        return ""
