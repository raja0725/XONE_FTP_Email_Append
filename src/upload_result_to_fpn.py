"""
Quick script to upload a result file to FPN destination folder
"""
import ftplib
from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables
load_dotenv()

def upload_result():
    """Upload the latest result file to FPN"""

    # FTP credentials
    server = os.getenv('FTP1_SERVER')
    username = os.getenv('FTP1_USERNAME')
    password = os.getenv('FTP1_PASSWORD')
    port = int(os.getenv('FTP1_PORT', 21))

    # Paths
    local_file = 'downloads/twenty_recordsemail_converted-results-1982152.csv'
    dest_dir = '/PreScreen Delivery/Fushia/to_FPN'

    if not os.path.exists(local_file):
        print(f"Error: File not found: {local_file}")
        return

    try:
        # Connect to FTP
        print(f"Connecting to {server}...")
        ftp = ftplib.FTP_TLS()
        ftp.connect(server, port)
        ftp.login(username, password)
        ftp.prot_p()
        print("Connected successfully!")

        # Check if destination directory exists
        try:
            ftp.cwd(dest_dir)
            print(f"Destination directory exists: {dest_dir}")
        except:
            print(f"Destination directory not accessible: {dest_dir}")
            print("Trying to create it...")
            try:
                ftp.mkd(dest_dir)
                print("Directory created!")
                ftp.cwd(dest_dir)
            except Exception as e:
                print(f"Could not create directory: {e}")
                print("Uploading to root instead...")
                ftp.cwd('/')

        # Upload the file
        filename = Path(local_file).name
        remote_path = f"{dest_dir}/{filename}"

        print(f"\nUploading {filename}...")
        print(f"  From: {local_file}")
        print(f"  To: {remote_path}")

        with open(local_file, 'rb') as f:
            ftp.storbinary(f'STOR {filename}', f)

        print(f"\n[SUCCESS] File uploaded successfully!")
        print(f"Result file is now available at: {remote_path}")

        ftp.quit()

    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    upload_result()
