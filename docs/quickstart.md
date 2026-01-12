# Quick Start

## Basic Usage

### 1. Create Configuration

Create a `config.yml` file in the project root (refer to `config.example.yml`):

```yaml
notification:
  smtp:
    host: smtp.gmail.com
    port: 587
    username: your_email@gmail.com
    password: your_password
    from_email: your_email@gmail.com
    default_receive_email: default@example.com
    default_template_file: birthday.html
    default_reminder_days: 7

  serverchan:
    default_sckey: your_sckey
    default_reminder_days: 7

  start_notification: "email,serverchan"

recipients:
  - name: "John Doe"
    solar_birthday: "1990-05-15"
    email: john@example.com
    reminder_days: 7
    template_file: birthday.html

  - name: "Jane Smith"
    lunar_birthday: "1988-03-20"
    email: jane@example.com
    reminder_days: 7
```

### 2. Run Locally

```bash
# Run birthday reminder
python -m src.main run --config config.yml

# Preview email
python -m src.main preview --config config.yml
```

### 3. Deploy with GitHub Actions

1. Fork the repository
2. Set repository secret `BIRTHDAY_YAML` with your config content
3. Go to Actions and run "Daily Birthday Check"

### 4. Deploy with Docker

```bash
# Run with Docker
docker run -v ${PWD}/config.yml:/app/config.yml ghcr.io/wllzhang/birthdayrs:latest run

# Preview with Docker
docker run -v ${PWD}/config.yml:/app/config.yml -v ${PWD}/previews:/app/previews ghcr.io/wllzhang/birthdayrs:latest preview
```

## Commands

### Run Birthday Check

```bash
python -m src.main run --config config.yml
```

### Preview Email

```bash
python -m src.main preview --config config.yml
```

### Validate Configuration

```bash
python -m src.main validate --config config.yml
```

### Show Application Info

```bash
python -m src.main info --config config.yml
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test
pytest tests/test_main.py
```
