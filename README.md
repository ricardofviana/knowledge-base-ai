# Knowledge Base AI

A Python-based tool that extracts content from articles, generates AI-powered summaries, and integrates them into Notion as a personal knowledge base.

## Features

- Article content extraction from web pages
- AI-powered summarization using OpenAI's GPT models
- Automatic integration with Notion for organizing summaries
- Caching system for processed articles
- Error handling and logging

## Requirements

- Python 3.8+
- OpenAI API key
- Notion API key

## Installation

1. Clone the repository
```bash
git clone [repository-url]
cd knowledge-base-ai
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies
```bash 
pip install -r requirements.txt
```

4. Configure environment variables
Create a `.env` file in the root directory with:
```
OPENAI_API_KEY=your_openai_api_key
NOTION_API_KEY=your_notion_api_key
CACHE_DIR=./cache
PROJECT_ROOT=/path/to/project
```

## Usage

[Usage instructions to be added]

## Project Structure

```
knowledge-base-ai/
├── src/
│   ├── ai_agent.py          # AI summarization logic
│   ├── notion_integration.py # Notion API integration
│   └── text_extractor.py    # Content extraction utilities
├── tests/
│   └── test_ai_agent.py     # Unit tests
├── cache/                   # Cache directory for processed articles
```