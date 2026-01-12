# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BirthdayRS is a birthday reminder system that supports both lunar (Chinese) and solar (Gregorian) calendar birthdays. It sends notifications via email and ServerChan, providing rich Chinese traditional culture information including zodiac signs, GanZhi (干支), festivals, and solar terms.

## Common Commands

### Development
```bash
# Install dependencies (using uv)
uv sync

# Install dependencies (using pip)
pip install -r requirements.txt

# Run the application
python -m src.main run --config config.yml

# Preview email template
python -m src.main preview

# Validate configuration
python -m src.main validate --config config.yml

# Show application info
python -m src.main info --config config.yml
```

### Testing
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src

# Run tests with HTML coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_main.py
```

### Code Quality
```bash
# Run flake8 linter
flake8 .

# Flake8 configuration is in .flake8
# - Max line length: 100
# - Ignores: E501, W503
```

### Docker
```bash
# Build Docker image
docker build -t birthdayrs .

# Run with Docker
docker run -v ${PWD}/config.yml:/app/config.yml birthdayrs run

# Preview with Docker
docker run -v ${PWD}/config.yml:/app/config.yml -v ${PWD}/previews:/app/previews birthdayrs preview
```

## Architecture

### Core Components

**BirthdayReminder** (`src/main.py`)
- Main application entry point
- Orchestrates birthday checking and notification sending
- Uses asyncio for concurrent notification delivery
- CLI interface built with Click

**ConfigManager** (`src/core/config_manager.py`)
- Handles YAML config loading and validation
- Provides default config path resolution
- Returns templates directory path

**BirthdayChecker** (`src/core/checker.py`)
- Checks birthdays against current date with advance reminder support
- Handles both solar and lunar calendar conversions using `lunar_python` library
- Generates rich date information: GanZhi, zodiac, festivals, solar terms, constellations
- Returns tuple of (Recipient, is_birthday, extra_info) for each recipient

**NotificationFactory** (`src/core/notification_factory.py`)
- Factory pattern for creating notification senders
- Supports multiple notification types: email, serverchan
- Creates senders based on config.notification_types list

**NotificationBase** (`src/notification/notification_base.py`)
- Abstract base class for all notification senders
- Defines interface: `render_content()` and `send()`

**EmailSender** (`src/notification/sender_email.py`)
- Sends HTML emails via SMTP using aiosmtplib
- Uses Jinja2 templates from `templates/` directory
- Includes retry decorator with exponential backoff (3 retries, 1s initial delay, 2x backoff)
- Preview functionality generates HTML files in `previews/` directory

**ServerChanSender** (`src/notification/sender_serverchan.py`)
- Sends notifications via ServerChan API
- Uses httpx for async HTTP requests

### Configuration Flow

1. ConfigManager loads `config.yml` (or path from `--config` option)
2. Config.from_yaml() parses YAML and applies defaults:
   - SMTP defaults: `default_receive_email`, `default_template_file`, `default_reminder_days`
   - ServerChan defaults: `default_sckey`, `default_reminder_days`
3. Recipients inherit defaults if not explicitly set
4. NotificationFactory creates senders based on `notification_types` list

### Birthday Check Flow

1. BirthdayChecker iterates through recipients
2. For each recipient, checks dates from today to (today + reminder_days)
3. Compares solar_birthday (month/day match) and lunar_birthday (using lunar_python)
4. Extracts rich date info: GanZhi, zodiac, festivals, solar terms, week, constellation
5. Returns results with extra_info dict containing all date metadata

### Notification Flow

1. BirthdayReminder.run() calls check_birthdays()
2. For each birthday match, creates async task for send_birthday_reminder()
3. Tasks run concurrently via asyncio.gather()
4. Each notification sender:
   - Renders Jinja2 template with recipient name and extra_info
   - Sends via specific channel (email/serverchan)
   - Retries on failure (email only)

## Configuration Structure

The `config.yml` must include:
- `notification.smtp` - SMTP server settings for email
- `notification.serverchan` - ServerChan API key
- `notification.start_notification` - Comma-separated list: "email", "serverchan", or "email,serverchan"
- `recipients` - List of recipients with:
  - `name` (required)
  - `solar_birthday` and/or `lunar_birthday` (at least one required, format: YYYY-MM-DD)
  - `email` (optional if default_receive_email set)
  - `reminder_days` (optional, defaults from smtp/serverchan config)
  - `template_file` (optional, defaults to birthday.html)

## Important Notes

- Lunar birthdays in config are stored as their solar (Gregorian) equivalent dates
- The lunar_python library handles conversion between solar and lunar calendars
- Templates use Jinja2 and are located in `templates/` directory
- Email retry logic uses exponential backoff to handle transient SMTP failures
- All notification senders run concurrently for performance
- The application logs to both stdout and `birthday_reminder.log`
- Tests use pytest with async support (pytest-asyncio)
- CI/CD pipeline runs on GitHub Actions: lint → test → docker build/push
- Python version: 3.10+ (specified in pyproject.toml as >=3.8, but CI uses 3.10)
