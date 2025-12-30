"""
Test Email and Slack Notifications
Quick test script to verify notification setup
"""

import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from datetime import datetime

# Load environment variables
load_dotenv()

def test_email_notification():
    """Test email notification"""
    print("\n" + "="*70)
    print("TESTING EMAIL NOTIFICATION")
    print("="*70)

    try:
        email_from = os.getenv('EMAIL_FROM')
        email_to = os.getenv('EMAIL_TO')
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = int(os.getenv('SMTP_PORT', 587))
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')

        print(f"From: {email_from}")
        print(f"To: {email_to}")
        print(f"SMTP Server: {smtp_server}:{smtp_port}")
        print(f"Username: {smtp_username}")

        # Create test email
        msg = MIMEMultipart('alternative')
        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = "TEST: FPN Email Append Notification System"

        # HTML body
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .header {{ background-color: #28a745; color: white; padding: 15px; }}
                .content {{ padding: 20px; }}
                .success {{ color: #28a745; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>Notification Test Successful!</h2>
            </div>
            <div class="content">
                <p><strong>Test Status:</strong> <span class="success">SUCCESS</span></p>
                <p><strong>Test Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>This is a test email from the FPN Email Append Processor.</p>
                <p>If you're seeing this, your email notifications are configured correctly!</p>
                <hr>
                <p><em>Configured by: Yeswanth Raja</em></p>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_body, 'html'))

        # Send email
        print("\nConnecting to SMTP server...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            print("Logging in...")
            server.login(smtp_username, smtp_password)
            print("Sending email...")
            server.send_message(msg)

        print(f"\n[SUCCESS] Email sent to {email_to}")
        print("   Check your inbox at support@accelerated.com!")
        return True

    except Exception as e:
        print(f"\n[FAILED] Email notification failed: {str(e)}")
        return False

def test_slack_notification():
    """Test Slack notification"""
    print("\n" + "="*70)
    print("TESTING SLACK NOTIFICATION")
    print("="*70)

    try:
        webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        channel = os.getenv('SLACK_CHANNEL', '#Frank')

        print(f"Channel: {channel}")
        print(f"Webhook: {webhook_url[:50]}...")

        # Create test message
        slack_message = f"""*FPN Email Append Notification Test*

Status: SUCCESS
Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This is a test message from the FPN Email Append Processor.
If you're seeing this in {channel}, your Slack notifications are working!

_Configured by: Yeswanth Raja_
"""

        payload = {
            "channel": channel,
            "username": "FPN Email Processor",
            "icon_emoji": ":email:",
            "text": slack_message
        }

        # Send to Slack
        print("\nSending Slack message...")
        response = requests.post(webhook_url, json=payload, timeout=10)

        if response.status_code == 200:
            print(f"\n[SUCCESS] Slack message sent to {channel}")
            print("   Check the #Frank channel in Slack!")
            return True
        else:
            print(f"\n[FAILED] Slack notification failed: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"\n[FAILED] Slack notification failed: {str(e)}")
        return False

def main():
    """Run all notification tests"""
    print("\n" + "="*70)
    print("FPN EMAIL APPEND - NOTIFICATION SYSTEM TEST")
    print("="*70)
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Test email
    email_success = test_email_notification()

    # Test Slack
    slack_success = test_slack_notification()

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Email Notification: {'PASSED' if email_success else 'FAILED'}")
    print(f"Slack Notification: {'PASSED' if slack_success else 'FAILED'}")

    if email_success and slack_success:
        print("\nALL TESTS PASSED!")
        print("\nYour notification system is ready to use!")
        print("When files are processed, you will receive:")
        print("  - Email at support@accelerated.com")
        print("  - Slack message in #Frank channel")
    else:
        print("\nSOME TESTS FAILED")
        print("Please check the error messages above and fix the configuration.")

    print("\n" + "="*70)

if __name__ == "__main__":
    main()
