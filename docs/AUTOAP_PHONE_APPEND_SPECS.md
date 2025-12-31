# AutoAp Phone Append Process Specification

## Overview

AutoAp is a recall processing service for automotive dealerships and marketing companies. This document describes the automated phone append workflow that processes recall data through our FTP system.

## Business Context

### What AutoAp Does
- Processes vehicle recalls for automotive dealerships and marketing companies
- Two data sources:
  1. **Dealership Customer Data**: Existing customers of the dealership
  2. **DataVast Data**: Prospective customers (people who own vehicles but are not current dealership customers)

### Why This Matters
- Helps dealerships reach vehicle owners who have recalls
- Expands dealership customer base by identifying new prospects with recalled vehicles
- Requires phone append to ensure contact information is current and complete

## Process Flow

### 1. Data Acquisition (AutoAp Side)
```
AutoAp → DataVast API
```
- AutoAp connects to our DataVast API
- Pulls subset of people based on:
  - Geographic radius around the dealership
  - Vehicle make
- Downloads vehicle owner data
- Checks each vehicle for active recalls

### 2. File Drop to Xcelerated FTP
```
AutoAp → Xcelerated FTP (Incoming)
```
- AutoAp creates comma-delimited file with recall vehicles
- File contains vehicle owners needing phone append
- Dropped to designated FTP folder for processing

### 3. File Formatting for Data Axle
```
Xcelerated FTP → Format Conversion → Data Axle Format
```
**Our Responsibility:**
- Pick up file from FTP incoming folder
- Transform/format file to Data Axle specifications
- Validate data format and structure

### 4. Upload to Data Axle
```
Formatted File → Data Axle FTP (Phone Append Service)
```
**Our Responsibility:**
- Upload formatted file to Data Axle FTP folder
- Data Axle performs phone append processing
- Monitor for completion

### 5. Download Appended Results
```
Data Axle FTP → Download Results
```
**Our Responsibility:**
- Monitor Data Axle FTP for completed file
- Download phone-appended results
- Validate append results

### 6. Format for AutoAp Return
```
Data Axle Results → Format Conversion → AutoAp Format
```
**Our Responsibility:**
- Transform Data Axle results to AutoAp's expected format
- Include appended phone numbers
- Maintain data integrity

### 7. Drop to Xcelerated FTP for Pickup
```
Formatted Results → Xcelerated FTP (Outgoing)
```
**Our Responsibility:**
- Drop formatted file to FTP outgoing folder
- AutoAp monitors and picks up completed file
- Process complete

## Complete Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ AutoAp Process (Their Side)                                     │
├─────────────────────────────────────────────────────────────────┤
│ 1. Connect to DataVast API                                      │
│ 2. Pull vehicle owner data (radius + make filter)               │
│ 3. Check vehicles for recalls                                   │
│ 4. Create CSV file with recall vehicles                         │
│ 5. Drop file to Xcelerated FTP                                  │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ Xcelerated Automation (Our Side)                                │
├─────────────────────────────────────────────────────────────────┤
│ 1. Monitor FTP incoming folder                                  │
│ 2. Pick up AutoAp file                                          │
│ 3. Format file for Data Axle specifications                     │
│ 4. Upload to Data Axle FTP                                      │
│ 5. Monitor Data Axle for completion                             │
│ 6. Download phone-appended results                              │
│ 7. Format results for AutoAp specifications                     │
│ 8. Drop to FTP outgoing folder                                  │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ AutoAp Process (Their Side)                                     │
├─────────────────────────────────────────────────────────────────┤
│ 1. Monitor Xcelerated FTP                                       │
│ 2. Pick up phone-appended file                                  │
│ 3. Use appended data for recall outreach                        │
└─────────────────────────────────────────────────────────────────┘
```

## File Format Specifications

### Input File Format (AutoAp → Xcelerated)
**Format:** Comma-delimited CSV file

**Expected Fields:**
- To be documented based on AutoAp's file layout
- Contains vehicle owner information
- Requires phone append

**File Naming Convention:**
- To be documented

**File Location:**
- FTP incoming folder (path to be configured)

### Data Axle Format (Xcelerated → Data Axle)
**Format:** Data Axle-specific format

**Required Transformations:**
- Field mapping from AutoAp format to Data Axle format
- Data validation and cleansing
- Format standardization

**File Naming Convention:**
- To be documented per Data Axle requirements

**File Location:**
- Data Axle FTP folder (configured in .env)

### Output File Format (Xcelerated → AutoAp)
**Format:** Comma-delimited CSV file

**Expected Fields:**
- Original AutoAp data
- Appended phone numbers from Data Axle
- Match status indicators
- Any additional append metadata

**File Naming Convention:**
- To be documented

**File Location:**
- FTP outgoing folder (path to be configured)

## Technical Requirements

### FTP Configuration
```env
# AutoAp FTP (Our Server)
AUTOAP_FTP_SERVER=your.ftp.server.com
AUTOAP_FTP_USERNAME=username
AUTOAP_FTP_PASSWORD=password
AUTOAP_FTP_PORT=21
AUTOAP_INCOMING_DIR=/path/to/incoming/
AUTOAP_OUTGOING_DIR=/path/to/outgoing/

# Data Axle FTP
DATAAXLE_FTP_SERVER=dataaxle.ftp.server.com
DATAAXLE_FTP_USERNAME=username
DATAAXLE_FTP_PASSWORD=password
DATAAXLE_FTP_PORT=22
DATAAXLE_UPLOAD_DIR=/path/to/upload/
DATAAXLE_DOWNLOAD_DIR=/path/to/download/
```

### Processing Requirements
1. **File Monitoring**: Check for new files every X minutes
2. **Format Validation**: Validate input files before processing
3. **Error Handling**: Log and notify on processing errors
4. **Data Integrity**: Maintain record counts and validation
5. **Notifications**: Slack/email alerts for process status

### Dependencies
- Python 3.8+
- paramiko (SFTP operations)
- pandas (data processing)
- openpyxl (Excel operations if needed)
- python-dotenv (environment configuration)
- requests (Slack notifications)

## Automation Workflow

### Step-by-Step Process

1. **Monitor AutoAp FTP Incoming**
   - Check for new CSV files
   - Download to local processing directory
   - Archive original file

2. **Validate Input File**
   - Check file format
   - Validate required fields
   - Count records

3. **Transform to Data Axle Format**
   - Apply field mappings
   - Format phone numbers
   - Standardize addresses
   - Add required Data Axle fields

4. **Upload to Data Axle**
   - Connect to Data Axle FTP
   - Upload formatted file
   - Verify upload success
   - Log upload timestamp

5. **Monitor Data Axle Processing**
   - Check for result file
   - Wait with timeout
   - Download when available

6. **Transform to AutoAp Format**
   - Parse Data Axle results
   - Map to AutoAp expected format
   - Include append statistics
   - Generate match report

7. **Upload to AutoAp FTP Outgoing**
   - Format final file
   - Upload to outgoing folder
   - Verify upload
   - Send completion notification

8. **Logging and Reporting**
   - Log all processing steps
   - Generate processing report
   - Send Slack notification with stats
   - Archive processed files

## Error Handling

### Common Scenarios

1. **File Not Found**
   - Wait for next monitoring cycle
   - Alert if file expected but missing for X hours

2. **Invalid File Format**
   - Log error with details
   - Move file to error folder
   - Send alert to support team

3. **Data Axle Processing Failure**
   - Retry upload
   - Check Data Axle status
   - Alert if timeout exceeded

4. **FTP Connection Issues**
   - Retry with exponential backoff
   - Log connection errors
   - Alert if persistent failure

## Monitoring and Alerts

### Success Metrics
- Files processed per day
- Average processing time
- Phone append match rate
- Data Axle turnaround time

### Alert Conditions
- Processing errors
- File format issues
- FTP connection failures
- Data Axle timeout
- Unexpected delays

### Notification Channels
- Slack webhook for real-time alerts
- Email for critical failures
- Daily summary reports

## Security Considerations

1. **Credentials Management**
   - All FTP credentials in .env (never commit)
   - Use environment variables
   - Rotate passwords regularly

2. **Data Protection**
   - Encrypt sensitive data in transit
   - Secure local file storage
   - Delete processed files per retention policy

3. **Access Control**
   - Restrict FTP folder permissions
   - Monitor unauthorized access attempts
   - Audit file access logs

## Implementation Status

- [ ] File format specifications documented
- [ ] AutoAp FTP configuration
- [ ] Data Axle FTP configuration
- [ ] Format transformation logic
- [ ] Monitoring automation
- [ ] Error handling
- [ ] Notification system
- [ ] Testing with sample data
- [ ] Production deployment

## Related Documentation

- [Main README](../README.md) - Overall project documentation
- [FTP Email Processor](../src/ftp_email_processor.py) - Core processing logic
- [Notification Setup](NOTIFICATION_SETUP_GUIDE.md) - Slack integration
- [.env.example](../.env.example) - Environment configuration template

## Support and Maintenance

### Contact Information
- **Support Email**: support@xcelerated.com
- **Technical Lead**: [To be assigned]
- **AutoAp Contact**: [To be documented]
- **Data Axle Support**: [To be documented]

### Maintenance Schedule
- Daily monitoring of process logs
- Weekly review of append statistics
- Monthly review of error patterns
- Quarterly process optimization review

## Version History

- **v1.0** - Initial specification document (2024-12-30)
  - Documented workflow and process flow
  - Defined file format requirements
  - Established monitoring and alert procedures

---

**Document Owner**: Xcelerated LLC Development Team
**Last Updated**: 2024-12-30
**Status**: Specification Phase - Awaiting File Format Details
