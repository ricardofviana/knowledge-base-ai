# tests/test_ai_agent.py

import pytest
from unittest.mock import MagicMock
from src.ai_agent import generate_summary, ArticleSummaryRequest, client

def test_generate_summary_success(monkeypatch):
    """
    Test that generate_summary returns a valid ArticleSummaryRequest when the OpenAI API call succeeds.
    """
    article_text = "This is a sample article text for testing."
    
    # Create a fake ArticleSummaryRequest object (expected result)
    expected_summary = ArticleSummaryRequest(
        title="Test Title",
        summarized_text="This is a test summary for the article.",
        tags=["test", "article"]
    )
    
    # Create a fake message object with a 'parsed' attribute that holds our expected_summary
    fake_message = MagicMock()
    fake_message.parsed = expected_summary
    
    # Create a fake choice object that holds our fake_message
    fake_choice = MagicMock()
    fake_choice.message = fake_message
    
    # Create a fake response object with a 'choices' list containing our fake_choice
    fake_response = MagicMock()
    fake_response.choices = [fake_choice]
    
    # Define a fake parse function that returns our fake_response
    def fake_parse(*args, **kwargs):
        return fake_response

    # Monkeypatch the client's parse method with our fake_parse
    monkeypatch.setattr(client.beta.chat.completions, "parse", fake_parse)
    
    # Call the function under test
    result = generate_summary(article_text)
    
    # Assert that the result is as expected
    assert isinstance(result, ArticleSummaryRequest)
    assert result.title == "Test Title"
    assert result.summarized_text == "This is a test summary for the article."
    assert result.tags == ["test", "article"]

def test_generate_summary_failure(monkeypatch):
    """
    Test that generate_summary returns an empty string when an exception is raised during the API call.
    """
    article_text = "This is another sample article text."
    
    # Define a fake parse function that simulates an exception
    def fake_parse(*args, **kwargs):
        raise Exception("Simulated API failure")
    
    # Monkeypatch the client's parse method to simulate failure
    monkeypatch.setattr(client.beta.chat.completions, "parse", fake_parse)
    
    # Call the function under test
    result = generate_summary(article_text)
    
    # The function should return an empty string on exception
    assert result == ""