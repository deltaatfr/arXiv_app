# arXiv Paper Tracking System

A fully functional, portable arXiv paper tracking and analysis system that supports automatic crawling, downloading, information extraction, and intelligent analysis.

## Features

- **Automatic Crawling**: Automatically crawl latest paper information from the arXiv website
- **PDF Download**: Automatically download paper PDF files organized by date
- **Information Extraction**: Extract title, authors, abstract and other information from PDF files
- **Intelligent Analysis**: Use LLM for intelligent paper analysis and scoring
- **Report Generation**: Generate structured analysis reports
- **State Management**: Support for resumable operation and state recovery
- **Resource Monitoring**: Monitor system resource usage
- **Error Handling**: Comprehensive error handling and logging

## Quick Start

### 1. Environment Preparation

Ensure your system has Python 3.7 or higher installed.

### 2. Install Dependencies

```bash
# Method 1: Install directly using pip
pip install -r requirements.txt

# Method 2: Install using setup.py (recommended)
pip install -e .
```

### 3. Configure API Keys

Copy and edit the API configuration file:

```bash
cp config/api_config.json.example config/api_config.json
# Edit api_config.json and add your API keys
```

### 4. Run the System

```bash
# Basic usage
python arxivtracker.py --count 10

# Extract information from PDF files
python arxivtracker.py --count 10 --use-pdf

# Specify date
python arxivtracker.py --date 20260128 --count 15
```

## Usage Examples

### Command Line Usage

```bash
# Crawl and analyze 5 papers
arxiv-tracker --count 5

# Crawl only, no analysis
arxiv-tracker --count 10 --no-analysis

# Specify categories
arxiv-tracker --categories cs.AI,cs.LG --count 8
```

### Usage as a Python Library

```python
from arxiv_tracker import ArxivTracker

# Create tracker instance
tracker = ArxivTracker()

# Run tracking task
results = tracker.run(
    categories=['cs.AI', 'cs.LG'],
    count=10,
    use_pdf=True,
    date='20260128'
)

# View results
for paper in results:
    print(f"Title: {paper['title']}")
    print(f"Authors: {', '.join(paper['authors'])}")
    print(f"Score: {paper.get('score', 'N/A')}")
    print()
```

## Configuration Guide

### System Configuration

`config/system_config.json` contains system-level configuration:

- `data_dir`: Data storage directory
- `categories`: Default paper categories
- `max_workers`: Number of concurrent worker threads
- `timeout`: Network request timeout duration

### API Configuration

`config/api_config.json` contains API-related configuration:

- `dashscope_api_key`: Alibaba Cloud DashScope API key
- `api_endpoint`: API endpoint address
- `max_retries`: Maximum number of API request retries

## Dependencies

- Python 3.7+
- requests - Network requests
- beautifulsoup4 - HTML parsing
- PyPDF2 - PDF file processing
- psutil - System resource monitoring
- markdown - Markdown processing

## License

This project uses the MIT License.
