# Content Automation

## Description

A project designed to automate content creation and management workflows, streamlining repetitive tasks and improving efficiency.

## Features

- Automated content generation
- Workflow management
- File organization
- Batch processing

## Installation

```bash
git clone <repository-url>
cd Content_Automation
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

## Requirements

- Python 3.8+
- UV Package manager
- Dependencies listed in `requirements.txt`
- Node.js 14+ (for certain integrations)

## Configuration

Create a `.env` file in the project root with the following variables:

```
INSTAGRAM_ACCESS_TOKEN= instagram_access_code
```

Place your `client_secret.json` file to be download from the youtube api in the project root directory for authentication with youtube services.

## How It Works

The application uses Streamlit to provide a web interface for content automation. It processes user inputs, manages workflows through a queue system, and generates organized output files in batch operations

## Contributing

Pull requests are welcome. For major changes, please open an issue first.

## License

MIT
