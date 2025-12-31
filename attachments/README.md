# FTP Email Append Processor

A Python script for automated FTP file processing with email append tracking and reporting. This script is designed to work both standalone and as a Django management command.

## Features

- Downloads files from FTP server
- Converts pipe-delimited files to CSV format
- Uploads to email append service FTP
- Monitors processing completion
- Generates detailed Excel reports
- Tracks email statistics (new, duplicates, totals)
- Django-ready with management command support
- Secure credential management with environment variables

## Installation

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- **pandas**: For data processing and CSV handling
- **openpyxl**: For Excel report generation
- **python-dotenv**: For environment variable management

### 3. Configure Credentials

**IMPORTANT: Choose ONE method for credential management**

#### Method A: Environment Variables (RECOMMENDED - Most Secure)

1. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your actual credentials:
   ```
   FTP1_SERVER=your-ftp-server.com
   FTP1_USERNAME=your_username
   FTP1_PASSWORD=your_password

   FTP2_SERVER=email-append-server.com
   FTP2_USERNAME=append_username
   FTP2_PASSWORD=append_password
   ```

3. **NEVER commit `.env` to version control!** Add it to `.gitignore`:
   ```
   .env
   config.py
   ```

#### Method B: Direct Configuration File

1. Edit `config.py` directly and replace placeholder values
2. This method is less secure but simpler for testing

### How to Share Credentials Securely

**For Production/Team Sharing:**
1. Use a password manager (1Password, LastPass, BitWarden)
2. Use environment variables on your server
3. Use Django settings if integrated with Django
4. Use AWS Secrets Manager or Azure Key Vault for cloud deployments

**NEVER:**
- Email passwords in plain text
- Commit passwords to Git
- Share passwords in Slack/Teams messages

## Usage

### Standalone Execution

Run the script directly:

```bash
python ftp_email_processor.py
```

The script will:
1. Download file from first FTP server
2. Convert pipe-delimited format to CSV
3. Upload to email append FTP service
4. Wait for processing to complete
5. Download processed file
6. Generate Excel report with statistics

### Output Files

All output files are saved in the `output/` directory:

- **Converted CSV**: `*_converted.csv` - Pipe-to-CSV converted file
- **Excel Report**: `Email_Append_Report_YYYYMMDD_HHMMSS.xlsx` - Detailed statistics
- **Log File**: `ftp_processor.log` - Processing logs

### Excel Report Contents

The generated Excel report includes:

1. **Summary Sheet**:
   - Total records before/after
   - Email counts before/after appending
   - Number of new emails added
   - Number of duplicate emails found

2. **New Emails Sheet**:
   - Complete list of newly added email addresses

3. **Duplicates Sheet**:
   - List of duplicate email addresses (if any)

## Django Integration

### Setup Django Management Command

1. Create the management command structure in your Django app:

```
your_django_app/
├── management/
│   ├── __init__.py
│   └── commands/
│       ├── __init__.py
│       └── process_ftp_emails.py
```

2. Copy the Django management command file:

```bash
copy django_management_command.py your_django_app/management/commands/process_ftp_emails.py
```

3. Run from Django:

```bash
python manage.py process_ftp_emails
```

### Django Scheduled Tasks

Use Django-Cron or Celery for recurring execution:

#### Option 1: Django-Cron

```python
# your_app/cron.py
from django_cron import CronJobBase, Schedule

class FTPEmailProcessorCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440  # Run daily

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'your_app.ftp_email_processor'

    def do(self):
        from django.core.management import call_command
        call_command('process_ftp_emails')
```

#### Option 2: Celery Beat

```python
# celery.py
from celery import Celery
from celery.schedules import crontab

app = Celery('your_project')

app.conf.beat_schedule = {
    'process-ftp-emails-daily': {
        'task': 'your_app.tasks.process_ftp_emails',
        'schedule': crontab(hour=2, minute=0),  # Run at 2 AM daily
    },
}
```

## Configuration Options

Edit `config.py` or `.env` to customize:

| Setting | Description | Default |
|---------|-------------|---------|
| `ftp1_server` | First FTP server address | - |
| `ftp1_username` | First FTP username | - |
| `ftp1_password` | First FTP password | - |
| `source_filename` | Source file name on FTP | `Fushia_Upload_FPN.csv` |
| `ftp2_server` | Email append FTP server | - |
| `max_wait_minutes` | Max wait for processing | 30 |
| `check_interval` | Check interval in seconds | 60 |
| `download_dir` | Download directory | `./downloads` |
| `output_dir` | Output directory | `./output` |

## Troubleshooting

### Connection Issues

**Problem**: FTP connection fails
**Solution**:
- Verify FTP credentials are correct
- Check firewall settings
- Ensure FTP server is accessible from your network
- Try using passive mode if behind firewall

### File Not Found

**Problem**: Processed file not found after waiting
**Solution**:
- Increase `max_wait_minutes` in config
- Verify `processed_filename` matches what email append service generates
- Check FTP server logs

### Import Errors

**Problem**: `ModuleNotFoundError`
**Solution**:
```bash
pip install -r requirements.txt --upgrade
```

### Conversion Errors

**Problem**: Pipe delimiter not converting properly
**Solution**:
- Verify source file is actually pipe-delimited
- Check for escaped pipes in data
- Review log file for specific error

## Logging

All operations are logged to:
- Console (stdout)
- File: `ftp_processor.log`

Log levels:
- INFO: Normal operations
- WARNING: Non-critical issues
- ERROR: Failed operations

## Security Best Practices

1. **Never hardcode credentials** in Python files
2. **Use environment variables** for all sensitive data
3. **Add `.env` and `config.py`** to `.gitignore`
4. **Use FTPS (FTP over SSL)** when possible
5. **Rotate passwords regularly**
6. **Limit FTP user permissions** to required directories only

## Support

For issues or questions:
1. Check the log file: `ftp_processor.log`
2. Review this README
3. Contact your system administrator

## File Workflow

```
┌─────────────────┐
│  FTP Server 1   │
│  (Source Data)  │
└────────┬────────┘
         │ 1. Download
         ▼
┌─────────────────┐
│  Pipe-Delimited │
│      File       │
└────────┬────────┘
         │ 2. Convert
         ▼
┌─────────────────┐
│   CSV File      │
│  (Converted)    │
└────────┬────────┘
         │ 3. Upload
         ▼
┌─────────────────┐
│  FTP Server 2   │
│ (Email Append)  │
└────────┬────────┘
         │ 4. Process
         │ 5. Download
         ▼
┌─────────────────┐
│  Appended File  │
│  (with emails)  │
└────────┬────────┘
         │ 6. Analyze
         ▼
┌─────────────────┐
│  Excel Report   │
│  (for Laura)    │
└─────────────────┘
```

## License

Proprietary - Internal Use Only
