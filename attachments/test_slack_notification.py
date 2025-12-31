"""
Quick test script to verify Slack notifications are working
"""
from ftp_email_processor import FTPEmailProcessor
from config import FTP_CONFIG

# Create processor instance
processor = FTPEmailProcessor(FTP_CONFIG)

# Send a test notification
print("Sending test Slack notification...")
processor.send_slack_notification(
    message="This is a test notification to verify Slack integration is working correctly!",
    title="Test Notification"
)
print("Done! Check your #system-alerts channel in Slack.")
