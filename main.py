import argparse
from src.text_extractor import get_article_text
from src.ai_agent import generate_summary
from src.notion_integration import send_to_notion


def process_article(url: str) -> bool:
    """
    Process article from URL through the complete pipeline:
    1. Extract text from URL
    2. Generate AI summary
    3. Send to Notion

    Args:
        url (str): The URL of the article to process

    Returns:
        bool: True if successful, False otherwise
    """
    print(f"\nExtracting text from {url}...")
    article_text = get_article_text(url=url, use_cache=False)
    if not article_text:
        print("Error: No article text extracted")
        return False

    # Step 2: Generate AI summary
    print("\nGenerating AI summary...")
    summary = generate_summary(article_text)
    if not summary:
        print("Error: Failed to generate summary")
        return False

    print("\nGenerated Summary:")
    print("-" * 50)
    print(summary)
    print("-" * 50)

    # Step 3: Send to Notion
    print("\nSending to Notion...")
    notion_response = send_to_notion(
        summarized_text=summary.summarized_text,
        title=summary.title,
        url=url,
        tags=summary.tags
    )
    if notion_response:
        print("\nSuccessfully sent to Notion!")
        return True
    return False


def main():
    """Main function to process an article from a URL.

    This function sets up command-line argument parsing for article processing.
    It expects a URL as input and processes the article using the process_article function.

    Returns:
        None. Exits with status code 1 if processing fails, 0 if successful.

    Example:
        $ python main.py -u https://example.com/article
    """
    parser = argparse.ArgumentParser(
        description="Process an article: extract text, generate AI summary, and save to Notion"
    )
    parser.add_argument(
        "-u", "--url",
        required=True,
        help="URL of the article to process"
    )

    args = parser.parse_args()
    success = process_article(args.url)

    if success:
        print("\nArticle processing completed successfully!")
    else:
        print("\nArticle processing failed!")
        exit(1)


if __name__ == "__main__":
    main()
