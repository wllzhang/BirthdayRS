# Configuration

## Configuration File Structure

The `config.yml` file is the main configuration file for BirthdayRS. It contains settings for notifications and recipients.

## Notification Settings

### SMTP Configuration

```yaml
notification:
  smtp:
    host: smtp.gmail.com              # SMTP server host
    port: 587                          # SMTP server port
    username: your_email@gmail.com     # SMTP username
    password: your_password            # SMTP password
    from_email: your_email@gmail.com   # Sender email
    default_receive_email: default@example.com  # Default recipient
    default_template_file: birthday.html         # Default email template
    default_reminder_days: 7           # Default advance reminder days
```

### ServerChan Configuration

```yaml
notification:
  serverchan:
    default_sckey: your_sckey          # ServerChan API key
    default_reminder_days: 7           # Default advance reminder days
```

### Notification Types

```yaml
notification:
  start_notification: "email,serverchan"  # Comma-separated list
```

Available values:
- `email` - Send email notifications
- `serverchan` - Send ServerChan notifications
- `email,serverchan` - Send both types

## Recipients Configuration

### Recipient Fields

Each recipient can have the following fields:

```yaml
recipients:
  - name: "Recipient Name"             # Required: Recipient name
    solar_birthday: "1990-05-15"       # Optional: Solar birthday (YYYY-MM-DD)
    lunar_birthday: "1988-03-20"       # Optional: Lunar birthday (YYYY-MM-DD)
    email: recipient@example.com       # Optional: Email address
    reminder_days: 7                   # Optional: Advance reminder days
    template_file: birthday.html       # Optional: Email template file
```

### Multiple Recipients

```yaml
recipients:
  - name: "John Doe"
    solar_birthday: "1990-05-15"
    email: john@example.com

  - name: "Jane Smith"
    lunar_birthday: "1988-03-20"
    email: jane@example.com
    reminder_days: 14

  - name: "Bob Johnson"
    solar_birthday: "1985-12-25"
    email: bob@example.com
    template_file: custom.html
```

## Default Values

Recipients will inherit default values if not explicitly set:

- `email` - Inherits from `notification.smtp.default_receive_email`
- `reminder_days` - Inherits from SMTP or ServerChan defaults
- `template_file` - Inherits from `notification.smtp.default_template_file`

## Birthday Formats

### Solar Birthday

```yaml
solar_birthday: "1990-05-15"  # YYYY-MM-DD format
```

### Lunar Birthday

```yaml
lunar_birthday: "1988-03-20"  # Stored as solar equivalent
```

**Note**: Lunar birthdays in the config are stored as their solar (Gregorian) equivalent dates. The system uses the `lunar_python` library to handle conversions.

## Email Templates

Email templates use Jinja2 and are located in the `templates/` directory.

### Template Variables

Available variables in templates:
- `recipient` - Recipient information
- `extra_info` - Rich date information including:
  - `gan_zhi` - GanZhi for year, month, day, hour
  - `zodiac` - Chinese zodiac sign
  - `lunar_festivals` - Lunar festivals
  - `solar_festivals` - Solar festivals
  - `solar_terms` - Solar terms
  - `week` - Weekday information
  - `constellation` - Constellation information

### Custom Template

```yaml
recipients:
  - name: "John Doe"
    solar_birthday: "1990-05-15"
    template_file: custom.html
```

## Example Configuration

See `config.example.yml` in the project root for a complete example configuration.
