import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file if available
load_dotenv()

# Set your Notion API key and the page ID you want to query
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
PAGE_ID = "18e98b0b4a1981df9898dc300116b39c"

# Define the endpoint for retrieving a page
GET_PAGE_URL = f"https://api.notion.com/v1/blocks/{PAGE_ID}/children"

# Set up the headers required by the Notion API
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28"
}

def get_page_details():
    """
    Makes a GET request to the Notion API to retrieve details of a page.
    """
    response = requests.get(GET_PAGE_URL, headers=HEADERS)
    if response.status_code == 200:
        print("Page retrieved successfully:")
        print(response.json())
    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    get_page_details()
