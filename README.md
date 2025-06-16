# Birthday Reminder System
[![Docker Image](https://img.shields.io/badge/docker%20image-ghcr.io/wllzhang/birthdayrs-blue)](https://github.com/wllzhang/BirthdayRS/pkgs/container/birthdayrs)
[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Code Style](https://img.shields.io/badge/code%20style-flake8-black.svg)](https://flake8.pycqa.org/)

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
![GitHub last commit](https://img.shields.io/github/last-commit/wllzhang/BirthdayRS)
[![CI](https://github.com/wllzhang/BirthdayRS/actions/workflows/ci.yml/badge.svg)](https://github.com/wllzhang/BirthdayRS/actions/workflows/ci.yml)
[![Daily Check](https://github.com/wllzhang/BirthdayRS/actions/workflows/daily_check.yml/badge.svg)](https://github.com/wllzhang/BirthdayRS/actions/workflows/daily_check.yml)

![GitHub stars](https://img.shields.io/github/stars/wllzhang/BirthdayRS?style=social)
![GitHub forks](https://img.shields.io/github/forks/wllzhang/BirthdayRS?style=social)
![GitHub issues](https://img.shields.io/github/issues/wllzhang/BirthdayRS)

A powerful birthday reminder system that supports both lunar and solar calendar birthdays, providing rich Chinese traditional culture information.

[[中文文档](README.zh-CN.md)]  [[English Doc](README.md)] 

## Features

- **Dual Calendar Support**
  - [x] Support for solar (Gregorian) birthday reminders
  - [x] Support for lunar (Chinese) birthday reminders
  - [x] Smart handling of leap months

- **Rich Date Information**
  - [x] Display GanZhi (Heavenly Stems and Earthly Branches) for year, month, day, hour
  - [x] Display Chinese Zodiac
  - [x] Display lunar festivals
  - [x] Display solar festivals
  - [x] Display 24 solar terms
  - [x] Display weekday information
  - [x] Display constellation

- **Flexible Reminder Settings**
  - [x] Customizable advance reminder days
  - [x] Multiple recipient support
  - [x] Email notifications
  - [x] Email preview functionality
  - [x] Preview email
  - [x] Default settings
  - [x] GitHub Actions support
  - [X] Docker deployment
  - [X] Multiple notification sources (email, [ServerChan](https://sct.ftqq.com/))


## Configuration

Create a `config.yml` file in the project root directory (refer to `config.example.yml`)


## Usage

### 1. Local Run
#### Run
```bash
git clone https://github.com/wllzhang/BirthdayRS.git
cd BirthdayRS
# Install dependencies
pip install -r requirements.txt
# Local run
python -m src.main run
python -m src.main preview
```

#### View Help Information:
```bash
python -m src.main --help
python -m src.main preview --help
```

### 2. GitHub Action
   1. Fork the repository, set the variable `BIRTHDAY_YAML` in Settings with the content of your config.yaml
   2. Go to Actions and run the action: `Daily Birthday Check`
   
### 3. Docker Run

#### Available Tags
- `latest`: Latest stable version
- `vX.Y.Z`: Specific version (e.g., v1.0.0)
- `sha-XXXXXX`: Build for a specific commit

#### Run Examples

```bash
# Run birthday reminder
docker run -v ${PWD}/config.yml:/app/config.yml ghcr.io/wllzhang/birthdayrs:latest run
docker run -v ${PWD}/config.yml:/app/config.yml -v ${PWD}/previews:/app/previews  ghcr.io/wllzhang/birthdayrs:latest preview
```

## Email Templates

The system uses the Jinja2 template engine to render email content and supports custom email templates. The default template is located at `templates/birthday.html` and includes:

- Basic birthday information
- Lunar date information
- GanZhi (Heavenly Stems and Earthly Branches) for year, month, day, hour
- Zodiac and constellation
- Festival and solar term information
- Weekday information

## Testing

Run tests:
```bash
pytest
```
## License

MIT License

<details>

## Logging

System logs are saved in the `birthday_reminder.log` file, including:
- Configuration loading status
- Birthday check results
- Email sending status
- Error messages (if any)

## CI/CD Pipeline

This project uses GitHub Actions for a complete CI/CD pipeline:

### Continuous Integration (CI)

Each push or Pull Request will automatically run the following checks:

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
   - Automatically run birthday checks every day
   - Send reminder emails
   - Support for development and production environments

2. **Docker Deployment**
   - Quick deployment via Docker
   - Latest version image available

### Automation

- **README Auto-update**
  - Automatically update repository links in documentation
  - Keep documentation in sync with code
</details>
