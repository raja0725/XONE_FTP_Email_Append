"""
Configuration for FTP Email Processor
Using environment variables for security
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent

FTP_CONFIG = {
    # First FTP Server (Source)
    'ftp1_server': os.getenv('FTP1_SERVER', 'ftp.example.com'),
    'ftp1_username': os.getenv('FTP1_USERNAME', 'your_username'),
    'ftp1_password': os.getenv('FTP1_PASSWORD', 'your_password'),
    'ftp1_port': int(os.getenv('FTP1_PORT', 21)),

    # Source file configuration
    'source_filename': os.getenv('SOURCE_FILENAME', 'Fushia_Upload_FPN.csv'),
    'fpn_previous_dir': os.getenv('FPN_PREVIOUS_DIR', '/PreScreen Delivery/Fushia/from_FPN/previous/'),
    'fpn_destination_dir': os.getenv('FPN_DESTINATION_DIR', '/PreScreen Delivery/Fushia/to_FPN/'),
    'file_filter_keyword': os.getenv('FILE_FILTER_KEYWORD', 'email'),

    # Second FTP Server (Email Append Service)
    'ftp2_server': os.getenv('FTP2_SERVER', 'sftp2.towerdata.com'),
    'ftp2_username': os.getenv('FTP2_USERNAME', 'append_username'),
    'ftp2_password': os.getenv('FTP2_PASSWORD', 'append_password'),
    'ftp2_port': int(os.getenv('FTP2_PORT', 22)),

    # File processing configuration
    'upload_filename': os.getenv('UPLOAD_FILENAME', 'Fushia_Upload_FPN_converted.csv'),
    'processed_filename': os.getenv('PROCESSED_FILENAME', 'Fushia_Upload_FPN_appended.csv'),

    # Processing wait configuration
    'max_wait_minutes': int(os.getenv('MAX_WAIT_MINUTES', 30)),
    'check_interval': int(os.getenv('CHECK_INTERVAL', 60)),

    # Local directories
    'download_dir': os.getenv('DOWNLOAD_DIR', str(BASE_DIR / 'downloads')),
    'output_dir': os.getenv('OUTPUT_DIR', str(BASE_DIR / 'output')),

    # Email notification settings
    'send_email_notification': os.getenv('SEND_EMAIL_NOTIFICATION', 'False').lower() == 'true',
    'email_from': os.getenv('EMAIL_FROM', 'noreply@example.com'),
    'email_to': os.getenv('EMAIL_TO', 'support@example.com'),
    'email_subject': os.getenv('EMAIL_SUBJECT', 'FPN Email Append Processing Complete'),
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.getenv('SMTP_PORT', 587)),
    'smtp_username': os.getenv('SMTP_USERNAME', ''),
    'smtp_password': os.getenv('SMTP_PASSWORD', ''),

    # Slack notification settings
    'send_slack_notification': os.getenv('SEND_SLACK_NOTIFICATION', 'False').lower() == 'true',
    'slack_webhook_url': os.getenv('SLACK_WEBHOOK_URL', ''),
    'slack_channel': os.getenv('SLACK_CHANNEL', '#general'),
}

# Django-specific settings (optional - deprecated, use FTP_CONFIG instead)
DJANGO_SETTINGS = {
    'use_django_settings': os.getenv('USE_DJANGO_SETTINGS', 'False').lower() == 'true',
    'send_email_notification': os.getenv('SEND_EMAIL_NOTIFICATION', 'False').lower() == 'true',
    'notification_recipients': os.getenv('NOTIFICATION_RECIPIENTS', '').split(','),
    'notification_subject': os.getenv('NOTIFICATION_SUBJECT', 'Fushia FPN - Email Append Report Ready'),
}
