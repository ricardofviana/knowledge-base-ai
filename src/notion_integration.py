# src/notion_integration.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Selected variables from your current config:
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID =  os.getenv("DATABASE_ID")

# For creating pages, the endpoint is different from the BASE_URL used for databases.
CREATE_PAGE_URL = "https://api.notion.com/v1/pages"

# Set up the headers for Notion API requests:
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}


def send_to_notion(summarized_text, title="Article Summary", url=None, tags=None):
    """
    Create a new page in the Notion database with the provided summary and optional properties.

    Args:
        summary (str): The summary text (e.g., generated by your AI agent).
        title (str): The title for the page.
        url (str, optional): An optional URL to store (for example, a link to the original article).
        tags (list, optional): A list of tag names (strings) for the page.

    Returns:
        dict: The response from the Notion API, parsed as JSON.
    """
    # Build the payload with the required parent reference and properties.
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            }
        },
        "children": [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Summary"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": summarized_text
                            }
                        }
                    ]
                }
            }
        ]
    }

    # Include URL if provided
    if url:
        payload["properties"]["URL"] = {"url": url}

    # Include Tags if provided (each tag should be a dictionary with a "name" key)
    if tags:
        tags.append("Article")
        payload["properties"]["Tags"] = {
            "multi_select": [{"name": tag} for tag in tags]
        }

    # Send the POST request to create the page in Notion.
    response = requests.post(CREATE_PAGE_URL, headers=HEADERS, json=payload)

    if response.status_code in (200, 201):
        print("Page created successfully in Notion.")
        return response.json()
    else:
        print(f"Failed to create page in Notion: {response.status_code}")
        print(response.text)
        return response.json()


if __name__ == "__main__":
    # For testing purposes: sample data for creating a Notion page.
    sample_summary = (
        "This is a test summary generated by the AI agent. It covers the key takeaways of the article."
    )
    sample_title = "Test Article Summary"
    sample_tags = ["test", "AI"]
    sample_url = "https://example.com/article"

    notion_response = send_to_notion(
        summary=sample_summary,
        title=sample_title,
        url=sample_url,
        tags=sample_tags
    )
    print(notion_response)