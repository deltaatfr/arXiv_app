# arXiv Paper Tracking System

A fully functional, portable arXiv paper tracking and analysis system that supports automatic crawling, downloading, information extraction, and intelligent analysis.

## Directory Structure

```
arXiv_app/
├── README.md                           # Main project description
├── LICENSE                            # Open source license
├── requirements.txt                   # Dependency package list
├── pyproject.toml                     # Modern Python project configuration
├── setup.py                           # Traditional packaging configuration
├── arxivtracker.py                    # Main program entry point
├── config/                            # Configuration directory
│   ├── __init__.py
│   ├── system_config.json             # System configuration
│   ├── api_config.json                # API configuration template
│   ├── categories.json                # Paper categories
│   └── logging_config.json            # Logging configuration
├── src/                               # Source code (Python package compliant)
│   ├── __init__.py
│   ├── arxiv_tracker/                 # Main package
│   │   ├── __init__.py
│   │   ├── crawler.py                # Crawling module
│   │   ├── downloader.py             # Download module
│   │   ├── extractor.py              # Information extraction module
│   │   ├── analyzer.py               # Analysis module
│   │   ├── reporter.py               # Reporting module
│   │   ├── utils/                    # Utilities module
│   │   │   ├── __init__.py
│   │   │   ├── state_manager.py
│   │   │   ├── resource_monitor.py
│   │   │   ├── cache_manager.py
│   │   │   ├── file_utils.py
│   │   │   └── logger.py
│   │   └── data/                     # Data storage (relative path)
│   │       ├── papers/               # PDF files
│   │       ├── reports/              # Report files
│   │       ├── cache/                # Cache files
│   │       └── logs/                 # Log files
├── scripts/                           # Helper scripts
│   ├── __init__.py
│   ├── setup_venv.py                 # Environment setup (original step 0)
│   ├── reset_states.py               # State reset
│   ├── check_abstract.py             # Abstract checking
│   └── extract_from_pdf.py           # PDF extraction
├── docs/                              # Project documentation
│   ├── requirements.md               # Requirements document
│   ├── technical_design.md           # Technical design
│   ├── api_reference.md              # API reference
│   ├── installation.md               # Installation and deployment
│   ├── user_manual.md                # User manual
│   ├── maintenance.md                # Maintenance document
│   └── images/                       # Documentation images
├── tests/                             # Test files
│   ├── __init__.py
│   ├── conftest.py                   # pytest configuration
│   ├── test_crawler.py
│   ├── test_downloader.py
│   ├── test_extractor.py
│   ├── test_analyzer.py
│   └── integration/                  # Integration tests
├── examples/                          # Usage examples
│   ├── basic_usage.py
│   ├── custom_config.py
│   └── scheduled_task.py             # Scheduled task example
├── docker/                            # Docker configuration
│   ├── Dockerfile
│   └── docker-compose.yml
└── notebooks/                         # Jupyter Notebook examples
    └── demo_usage.ipynb
```

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

## Contributing

Issues and Pull Requests are welcome!

## Contact

- Project Repository: https://github.com/deltaatfr/arxiv-tracker
- Issue Reporting: https://github.com/deltaatfr/arxiv-tracker/issues
