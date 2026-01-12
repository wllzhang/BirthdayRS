# Installation

## Requirements

- Python 3.8 or higher
- pip or uv package manager

## Install from Source

```bash
# Clone the repository
git clone https://github.com/wllzhang/BirthdayRS.git
cd BirthdayRS

# Install dependencies using uv (recommended)
uv sync

# Or install using pip
pip install -r requirements.txt
```

## Development Installation

```bash
# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements.txt
```

## Docker Installation

```bash
# Pull the latest image
docker pull ghcr.io/wllzhang/birthdayrs:latest

# Or build from source
docker build -t birthdayrs .
```

## Verify Installation

```bash
# Check if the package is installed
python -m src.main --help

# Validate configuration
python -m src.main validate --config config.yml

# Show application info
python -m src.main info --config config.yml
```
