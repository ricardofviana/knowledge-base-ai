import pytest
from unittest.mock import patch, mock_open
import os
from .text_extractor import fetch_page

@pytest.fixture
def mock_cache_dir(tmp_path):
    return str(tmp_path)

@pytest.fixture
def mock_requests_get():
    with patch('requests.get') as mock_get:
        yield mock_get

def test_fetch_page_without_cache(mock_requests_get, mock_cache_dir):
    # Arrange
    url = "http://example.com"
    mock_response = mock_requests_get.return_value
    mock_response.text = "<html>Test content</html>"
    
    # Act
    result = fetch_page(url, use_cache=False, cache_dir=mock_cache_dir)
    
    # Assert
    assert result == "<html>Test content</html>"
    mock_requests_get.assert_called_once_with(url)

def test_fetch_page_with_cache_miss(mock_requests_get, mock_cache_dir):
    # Arrange
    url = "http://example.com"
    mock_response = mock_requests_get.return_value
    mock_response.text = "<html>Test content</html>"
    
    # Act
    result = fetch_page(url, use_cache=True, cache_dir=mock_cache_dir)
    
    # Assert
    assert result == "<html>Test content</html>"
    mock_requests_get.assert_called_once_with(url)

def test_fetch_page_with_cache_hit(mock_requests_get, mock_cache_dir):
    # Arrange
    url = "http://example.com"
    cached_content = "<html>Cached content</html>"
    cache_file = os.path.join(mock_cache_dir, 
                             "1584b2cc1cda9a3f707d0fd5b2c326d2.html")
    
    os.makedirs(mock_cache_dir, exist_ok=True)
    with open(cache_file, 'w', encoding='utf-8') as f:
        f.write(cached_content)
    
    # Act
    result = fetch_page(url, use_cache=True, cache_dir=mock_cache_dir)
    
    # Assert
    assert result == cached_content
    mock_requests_get.assert_not_called()

def test_fetch_page_http_error(mock_requests_get, mock_cache_dir):
    # Arrange
    url = "http://example.com"
    mock_requests_get.return_value.raise_for_status.side_effect = Exception("HTTP Error")
    
    # Act & Assert
    with pytest.raises(Exception):
        fetch_page(url, use_cache=False, cache_dir=mock_cache_dir)