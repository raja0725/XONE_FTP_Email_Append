# Notification Setup Guide

Complete guide to configure email and Slack notifications for the FPN Email Append Processor.

## Overview

The processor can send notifications to:
1. **Email** (via SMTP) - Sends detailed HTML reports to support@accelerated.com
2. **Slack** (via Webhooks) - Sends quick summaries to #Frank channel

Notifications are sent when:
- Processing completes successfully
- Processing completes with some failures
- Processing fails completely

---

## Email Notification Setup

### 1. Configure SMTP Settings in .env

Open `.env` file and configure these settings:

```env
# Email Notification Settings
SEND_EMAIL_NOTIFICATION=True
EMAIL_FROM=noreply@accelerated.com
EMAIL_TO=support@accelerated.com
EMAIL_SUBJECT=FPN Email Append Processing Complete
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

### 2. SMTP Server Options

#### Option A: Gmail (Recommended for testing)

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Copy the generated 16-character password
3. Update .env:
   ```env
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your_email@gmail.com
   SMTP_PASSWORD=xxxx xxxx xxxx xxxx
   ```

#### Option B: Microsoft 365 / Outlook

```env
SMTP_SERVER=smtp.office365.com
SMTP_PORT=587
SMTP_USERNAME=your_email@company.com
SMTP_PASSWORD=your_password
```

#### Option C: Company SMTP Server

Contact your IT department for:
- SMTP server address
- Port number (usually 25, 465, or 587)
- Authentication credentials

```env
SMTP_SERVER=mail.yourcompany.com
SMTP_PORT=587
SMTP_USERNAME=your_username
SMTP_PASSWORD=your_password
```

### 3. Test Email Notifications

To disable email notifications temporarily:
```env
SEND_EMAIL_NOTIFICATION=False
```

---

## Slack Notification Setup

### 1. Create Slack Incoming Webhook

1. Go to https://api.slack.com/apps
2. Click "Create New App" → "From scratch"
3. Name: `FPN Email Processor`
4. Select your workspace
5. Click "Incoming Webhooks"
6. Toggle "Activate Incoming Webhooks" to ON
7. Click "Add New Webhook to Workspace"
8. Select the `#Frank` channel
9. Click "Allow"
10. Copy the Webhook URL (looks like: `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX`)

### 2. Configure Slack Settings in .env

```env
# Slack Notification Settings
SEND_SLACK_NOTIFICATION=True
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
SLACK_CHANNEL=#Frank
```

**Replace** `https://hooks.slack.com/services/YOUR/WEBHOOK/URL` with your actual webhook URL from step 1.

### 3. Test Slack Notifications

To disable Slack notifications temporarily:
```env
SEND_SLACK_NOTIFICATION=False
```

---

## Notification Content

### Email Notifications Include:

- **Summary Section:**
  - Processing status (SUCCESS/PARTIAL SUCCESS/FAILED)
  - Total files processed
  - Successful/failed counts
  - Total new emails added
  - Completion timestamp

- **Successfully Processed Files Table:**
  - Filename
  - Number of new emails added

- **Failed Files Table** (if any):
  - Filename
  - Error message

- **HTML Formatted** with color-coded status indicators

### Slack Notifications Include:

- Status emoji (✓, ⚠️, or ✗)
- Quick summary stats
- List of processed files with email counts
- List of failed files with errors (if any)

---

## Troubleshooting

### Email Not Sending

**Error: "Authentication failed"**
- Verify SMTP username and password are correct
- For Gmail, ensure you're using an App Password (not your regular password)
- Check if 2FA is enabled (required for Gmail App Passwords)

**Error: "Connection timeout"**
- Check SMTP_SERVER and SMTP_PORT are correct
- Verify firewall isn't blocking SMTP connections
- Try port 465 (SSL) instead of 587 (TLS)

**Error: "Sender address rejected"**
- Ensure EMAIL_FROM matches your SMTP_USERNAME for most providers
- Some servers require EMAIL_FROM to be a valid domain email

### Slack Not Posting

**Error: "invalid_auth" or "channel_not_found"**
- Regenerate the webhook URL in Slack
- Verify the webhook has permission to post to #Frank channel
- Check the webhook URL is copied correctly (no spaces)

**Messages Not Appearing**
- Verify SLACK_CHANNEL matches exactly (case-sensitive)
- Check if the channel still exists
- Ensure the webhook wasn't revoked

### Notifications Disabled

Check these settings in .env:
```env
SEND_EMAIL_NOTIFICATION=True  # Must be True
SEND_SLACK_NOTIFICATION=True  # Must be True
```

---

## Security Best Practices

1. **Never commit .env file** - It contains sensitive credentials
2. **Use App Passwords** for Gmail (never use your main password)
3. **Rotate credentials** periodically
4. **Restrict webhook** access to only the necessary channels
5. **Monitor logs** for failed notification attempts

---

## Testing the Setup

### Quick Test

1. Set both notifications to True in .env
2. Move a test file back to FPN source directory:
   ```bash
   python move_file_back.py
   ```
3. Run the processor:
   ```bash
   python ftp_email_processor.py
   ```
4. Check your email and Slack channel for notifications

### Expected Results

- **Email**: HTML-formatted report with green header (success)
- **Slack**: Message in #Frank channel with ✓ emoji and summary

---

## Notification Schedule

Notifications are sent:

1. **After workflow completes** - Whether successful, partial, or failed
2. **On critical errors** - If the entire workflow crashes
3. **Never during processing** - Only at the end to avoid spam

To receive notifications for each file as it's processed, contact support for custom configuration.

---

## Support

For issues with notifications:
- **Email problems**: Contact your IT/email administrator
- **Slack problems**: Contact your Slack workspace admin
- **Script problems**: Check `ftp_processor.log` for error details

---

## Configuration Summary

### Minimal Working Configuration (.env)

```env
# Email
SEND_EMAIL_NOTIFICATION=True
EMAIL_FROM=noreply@accelerated.com
EMAIL_TO=support@accelerated.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_gmail@gmail.com
SMTP_PASSWORD=your-app-password-here

# Slack
SEND_SLACK_NOTIFICATION=True
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/TXXXX/BXXXX/XXXXXXXX
SLACK_CHANNEL=#Frank
```

Replace placeholders with your actual values and you're ready to go!
