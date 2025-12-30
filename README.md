# FTP Email Processor

Automated system for processing files between FTP servers with email append service integration and comprehensive reporting.

## Overview

This application automates the workflow of downloading files from a source FTP server, processing them, uploading to an email append service, and generating detailed reports with Slack notifications.

## Features

- **Multi-Server FTP Operations**: Supports both standard FTP and SFTP protocols
- **Automated File Processing**: Downloads, converts, and uploads files automatically
- **Email Append Integration**: Integrates with TowerData email append service
- **Comprehensive Reporting**: Generates detailed Excel reports with statistics
- **Slack Notifications**: Real-time status updates via Slack webhooks
- **Error Handling**: Robust error handling with detailed logging
- **Django Integration Ready**: Can be integrated into Django projects

## Project Structure

```
ftp-email-processor/
├── src/                          # Source code
│   ├── ftp_email_processor.py   # Main processor class
│   ├── config.py                # Configuration module
│   └── upload_result_to_fpn.py  # Result upload handler
├── tests/                        # Test scripts
│   ├── test_notifications.py    # Notification testing
│   └── test_slack_notification.py
├── docs/                         # Documentation
│   ├── NOTIFICATION_IMPLEMENTATION_SUMMARY.md
│   ├── NOTIFICATION_SETUP_COMPLETE.md
│   └── NOTIFICATION_SETUP_GUIDE.md
├── data/                         # Data directories (gitignored)
│   ├── downloads/               # Downloaded files
│   └── output/                  # Processed files
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Prerequisites

- Python 3.8 or higher
- Access to source FTP server (FPN)
- Access to destination SFTP server (TowerData or similar)
- SMTP server access for email notifications
- Slack webhook URL (optional, for notifications)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ftp-email-processor.git
   cd ftp-email-processor
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual credentials
   ```

## Configuration

Edit the `.env` file with your credentials:

```env
# FTP Server 1 - Source
FTP1_SERVER=your.ftp.server.com
FTP1_USERNAME=username
FTP1_PASSWORD=password
FTP1_PORT=21

# FTP Server 2 - Destination
FTP2_SERVER=your.sftp.server.com
FTP2_USERNAME=username
FTP2_PASSWORD=password
FTP2_PORT=22

# File paths
SOURCE_FILENAME=/path/to/source/
FPN_PREVIOUS_DIR=/path/to/archive/
FPN_DESTINATION_DIR=/path/to/destination/
UPLOAD_FILENAME=output.csv

# Slack notifications (optional)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK
```

## Usage

### Basic Usage

```python
from src.ftp_email_processor import FTPEmailProcessor
from src.config import FTP_CONFIG

# Initialize processor
processor = FTPEmailProcessor()

# Run full workflow
processor.run_full_workflow()
```

### Command Line

```bash
python src/ftp_email_processor.py
```

### Testing Notifications

```bash
python tests/test_notifications.py
python tests/test_slack_notification.py
```

## Workflow

1. **Download**: Connects to FTP1 and downloads the latest file
2. **Process**: Converts and processes the file data
3. **Upload**: Uploads processed file to FTP2 (email append service)
4. **Monitor**: Waits for and downloads the processed result
5. **Archive**: Moves original file to archive directory on FTP1
6. **Upload Results**: Uploads final results back to FTP1
7. **Report**: Generates Excel report and sends Slack notification

## Features in Detail

### Email Append Processing
- Integrates with TowerData email append service
- Automatic result retrieval and processing
- Match rate calculation and reporting

### Reporting
- Generates comprehensive Excel reports
- Statistics include:
  - Total records processed
  - Email match rates
  - Processing timestamps
  - File information

### Notifications
- Real-time Slack notifications
- Success/failure status updates
- Processing statistics
- Error details when failures occur

### Error Handling
- Comprehensive logging to `ftp_processor.log`
- Automatic retry logic for transient failures
- Detailed error messages in notifications

## Security Notes

- **Never commit `.env` file** - Contains sensitive credentials
- Keep FTP credentials secure
- Use environment variables for all sensitive data
- Regularly rotate passwords
- Use SFTP instead of FTP when possible for encrypted transfers

## Django Integration

This application can be integrated into Django projects. See [docs/NOTIFICATION_IMPLEMENTATION_SUMMARY.md](docs/NOTIFICATION_IMPLEMENTATION_SUMMARY.md) for details.

## Logging

Logs are written to `ftp_processor.log` with the following format:
```
2024-12-30 10:30:00 - INFO - Starting file download from FTP1
2024-12-30 10:30:05 - INFO - Successfully downloaded: file.csv
```

## Troubleshooting

### Connection Issues
- Verify FTP credentials in `.env`
- Check firewall rules for ports 21 (FTP) and 22 (SFTP)
- Ensure network connectivity to FTP servers

### File Processing Issues
- Check file format matches expected CSV structure
- Verify file permissions in download/upload directories
- Review logs in `ftp_processor.log`

### Notification Issues
- Verify Slack webhook URL is correct
- Check internet connectivity
- Review notification test scripts

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

Internal use only - Xcelerated LLC

## Support

For questions or issues, contact: support@xcelerated.com

## Version History

- **v1.0.0** - Initial release with full FTP processing workflow
- Enhanced notification system with Slack integration
- Django-ready implementation
