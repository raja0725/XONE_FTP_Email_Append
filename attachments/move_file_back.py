"""
Helper script to move a file from previous/ back to from_FPN/ for testing
"""
import ftplib
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def move_file_back():
    """Move a file from previous/ folder back to source folder"""

    # FTP credentials
    server = os.getenv('FTP1_SERVER')
    username = os.getenv('FTP1_USERNAME')
    password = os.getenv('FTP1_PASSWORD')
    port = int(os.getenv('FTP1_PORT', 21))

    # Paths
    previous_dir = '/PreScreen Delivery/Fushia/from_FPN/Previous'
    source_dir = '/PreScreen Delivery/Fushia/from_FPN'

    try:
        # Connect to FTP
        print(f"Connecting to {server}...")
        ftp = ftplib.FTP_TLS()
        ftp.connect(server, port)
        ftp.login(username, password)
        ftp.prot_p()
        print("Connected successfully!")

        # List files in previous folder
        print(f"\nListing files in {previous_dir}...")
        ftp.cwd(previous_dir)
        files = ftp.nlst()

        if not files:
            print("No files found in previous/ folder")
            ftp.quit()
            return

        print(f"\nFound {len(files)} file(s):")
        for idx, f in enumerate(files, 1):
            print(f"  {idx}. {f}")

        # Find file with "email" keyword
        email_files = [f for f in files if 'email' in f.lower()]

        if email_files:
            filename = email_files[0]
            print(f"\nAuto-selecting file with 'email' keyword: {filename}")
        elif len(files) == 1:
            filename = files[0]
            print(f"\nMoving the only file: {filename}")
        else:
            # Just select the first file if no interactive input available
            filename = files[0]
            print(f"\nAuto-selecting first file: {filename}")

        # Move the file back
        source_path = f"{previous_dir}/{filename}"
        dest_path = f"{source_dir}/{filename}"

        print(f"\nMoving {filename}...")
        print(f"  From: {source_path}")
        print(f"  To: {dest_path}")

        ftp.rename(source_path, dest_path)

        print(f"\n[OK] File moved successfully!")
        print(f"\nYou can now run: python ftp_email_processor.py")

        ftp.quit()

    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    move_file_back()
