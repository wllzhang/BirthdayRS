 # Birthday Reminder System
[![Docker Image](https://img.shields.io/badge/docker%20image-ghcr.io/wllzhang/birthdayrs-blue)](https://github.com/wllzhang/BirthdayRS/pkgs/container/birthdayrs)
[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Code Style](https://img.shields.io/badge/code%20style-flake8-black.svg)](https://flake8.pycqa.org/)

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
![GitHub last commit](https://img.shields.io/github/last-commit/wllzhang/BirthdayRS)
[![CI](https://github.com/wllzhang/BirthdayRS/actions/workflows/ci.yml/badge.svg)](https://github.com/wllzhang/BirthdayRS/actions/workflows/ci.yml)
[![Daily Check](https://github.com/wllzhang/BirthdayRS/actions/workflows/daily_check.yml/badge.svg)](https://github.com/wllzhang/BirthdayRS/actions/workflows/daily_check.yml)

A powerful birthday reminder system that supports both solar and lunar calendar birthday reminders, with rich Chinese traditional cultural information.

[[中文文档](README.zh-CN.md)]  [[English Doc](README.md)] 

## Features

- **Dual Calendar Support**
  - [x] Solar calendar birthday reminders
  - [x] Lunar calendar birthday reminders
  - [x] Smart handling of leap months

- **Rich Date Information**
  - [x] Chinese Sexagenary Cycle (GanZhi) for year, month, day, and hour
  - [x] Chinese Zodiac signs
  - [x] Lunar festivals
  - [x] Solar festivals
  - [x] 24 Solar Terms
  - [x] Weekday information
  - [x] Western zodiac signs

- **Flexible Reminder Settings**
  - [x] Customizable advance reminder days
  - [x] Multiple recipient support
  - [x] Email notifications
  - [x] Email preview functionality
  - [x] Default settings
  - [x] GitHub Actions support
  - [x] Docker deployment
- **TODO**
  - [ ] Multiple notification channels support

## Configuration

Create a `config.yml` file in the project root directory (refer to `config.example.yml`), with the following format:

```yaml
smtp:
  host: smtp.example.com
  port: 587
  username: your_email@example.com
  password: your_password
  use_tls: true

recipients:
  - name: John Doe
    email: john@example.com
    solar_birthday: 1990-01-01  # Solar calendar birthday
    reminder_days: 3  # Remind 3 days in advance
  - name: Jane Doe
    email: jane@example.com
    lunar_birthday: 1995-02-15  # Lunar calendar birthday
    reminder_days: 7  # Remind 7 days in advance
```

## Usage

### 1. Local Run
#### Run
```bash
git clone https://github.com/wllzhang/BirthdayRS.git
cd BirthdayRS
# Install dependencies
pip install -r requirements.txt
# Run locally
python -m src.main run
```
#### Preview Email Content:
```bash
# Preview default test user's email
python -m src.main preview

# Preview specific recipient's email
python -m src.main preview --recipient "John Doe"

# Preview email for a specific date
python -m src.main preview --recipient "John Doe" --date "2024-01-01"
```
#### View Help Information:
```bash
python -m src.main --help
python -m src.main preview --help
```

### 2. GitHub Action
   1. Fork the repository and configure the `BIRTHDAY_YAML` variable in Settings with your config.yml content
   2. Go to Actions and run the `Daily Birthday Check` workflow

### 3. Docker Run

#### Available Tags
- `latest`: Latest stable version
- `vX.Y.Z`: Specific version (e.g., v1.0.0)
- `sha-XXXXXX`: Build for specific commit

#### Run Examples

```bash
# Run birthday reminder
docker run -v ${PWD}/config.yml:/app/config.yml ghcr.io/wllzhang/birthdayrs:latest run

# Preview email
docker run -v ${PWD}/config.yml:/app/config.yml \
           -v ${PWD}/previews:/app/previews \
           ghcr.io/wllzhang/birthdayrs:latest preview -r "Test User" -d "2024-01-01"
```

## Email Templates

The system uses Jinja2 template engine to render email content, supporting custom email templates. The default template is located at `templates/birthday.html` and includes:

- Basic birthday information
- Lunar date information
- Chinese Sexagenary Cycle (GanZhi)
- Zodiac signs and constellations
- Festival and solar term information
- Weekday information

## Testing

Run tests:
```bash
pytest
```

## Logging

System logs are saved in the `birthday_reminder.log` file, including:
- Configuration loading status
- Birthday check results
- Email sending status
- Error messages (if any)

## CI/CD Pipeline

This project uses GitHub Actions for a complete CI/CD pipeline:

### Continuous Integration (CI)

The following checks run automatically on each push or Pull Request:

1. **Code Testing**
   - Run unit tests
   - Generate test coverage report
   - Save test results as artifacts

2. **Code Quality**
   - Code style check with flake8
   - Ensure code follows PEP 8 standards

3. **Docker Image Build**
   - Automatically build Docker image
   - Push to GitHub Container Registry

### Continuous Deployment (CD)

1. **Daily Check**
   - Automatically run birthday checks
   - Send reminder emails
   - Support for development and production environments

2. **Docker Deployment**
   - Quick deployment via Docker
   - Latest version image available

### Automation

- **README Auto-update**
  - Automatically update repository links in documentation
  - Keep documentation in sync with code

## License

MIT License