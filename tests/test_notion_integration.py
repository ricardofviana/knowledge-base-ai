import pytest
from unittest.mock import patch, Mock
from src.notion_integration import send_to_notion

@pytest.fixture
def mock_response():
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {"id": "test-page-id"}
    return mock

def test_send_to_notion_basic(mock_response):
    with patch('requests.post', return_value=mock_response):
        response = send_to_notion("Test summary", "Test title")
        assert response == {"id": "test-page-id"}

def test_send_to_notion_with_url(mock_response):
    with patch('requests.post', return_value=mock_response):
        response = send_to_notion(
            "Test summary",
            "Test title", 
            url="https://example.com"
        )
        assert response == {"id": "test-page-id"}

def test_send_to_notion_with_tags(mock_response):
    with patch('requests.post', return_value=mock_response):
        response = send_to_notion(
            "Test summary",
            "Test title",
            tags=["tag1", "tag2"]
        )
        assert response == {"id": "test-page-id"}

def test_send_to_notion_failed():
    mock_failed = Mock()
    mock_failed.status_code = 400
    mock_failed.json.return_value = {"error": "Bad request"}
    mock_failed.text = "Error message"
    
    with patch('requests.post', return_value=mock_failed):
        response = send_to_notion("Test summary", "Test title")
        assert response == {"error": "Bad request"}

def test_send_to_notion_all_params(mock_response):
    with patch('requests.post', return_value=mock_response):
        response = send_to_notion(
            "Test summary",
            "Test title",
            url="https://example.com",
            tags=["tag1", "tag2"]
        )
        assert response == {"id": "test-page-id"}