import os
import hashlib
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


# Define a default cache directory relative to this file
load_dotenv()
DEFAULT_CACHE_DIR = os.getenv('CACHE_DIR')

def get_cache_filename(url, cache_dir=DEFAULT_CACHE_DIR, ext=".html"):
    """
    Generate a cache filename for a given URL using its MD5 hash.
    """
    url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
    return os.path.join(cache_dir, f"{url_hash}"+ext)

def fetch_page(url, use_cache=True, cache_dir=DEFAULT_CACHE_DIR):
    """
    Fetch the content of a webpage. If caching is enabled, check for a cached version first.
    Returns the HTML content as a string.
    """
    if use_cache:
        # Create cache directory if it doesn't exist
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        cache_file = get_cache_filename(url, cache_dir)
        # If the cache file exists, load and return its content
        if os.path.exists(cache_file):
            print(f"Loading content from cache for URL: {url}")
            with open(cache_file, 'r', encoding='utf-8') as f:
                return f.read()

    # If no cache is used or cache miss, fetch the content from the URL
    print(f"Fetching content from URL: {url}")
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    html_content = response.text

    # Save to cache if enabled
    if use_cache:
        with open(cache_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

    return html_content

def extract_text(html_content):
    """
    Extract and clean text from HTML content using BeautifulSoup.
    This basic implementation strips out scripts, styles, and extra whitespace.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove unwanted elements
    for element in soup(["script", "style"]):
        element.decompose()
    
    # Extract text and collapse extra whitespace
    text = soup.get_text(separator=' ')
    text = ' '.join(text.split())
    return text

def get_article_text(url, use_cache=True):
    """
    Fetch and extract the main text content from a given URL.
    """
    html_content = fetch_page(url, use_cache=use_cache)
    article_text = extract_text(html_content)
    return article_text

if __name__ == "__main__":
    # Simple CLI testing: provide a URL as an argument to test extraction.
    import sys
    if len(sys.argv) < 2:
        print("Usage: python text_extractor.py <url>")
        sys.exit(1)
    url = sys.argv[1]
    #Tinha usado essa parte para textar retorno do texto completo
    # text = get_article_text(url)
    # text_file_name = get_cache_filename(url, cache_dir=DEFAULT_CACHE_DIR, ext=".text")
    # with open(text_file_name, 'w', encoding='utf-8') as f:
    #         f.write(text)
    print("\nExtracted Text (first 500 characters):\n")
    print(text[:500])
