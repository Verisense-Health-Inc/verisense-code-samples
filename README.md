# AWS S3 File Downloader

This Python script is designed to download files from a specified AWS S3 bucket. It targets specific object key prefixes, making it suitable for scenarios where only certain directories or file types need to be downloaded.

## Features

- Configurable for any S3 bucket and object key prefixes.
- Downloads files while maintaining the S3 directory structure.
- Utilizes environment file for AWS credentials for enhanced security.

## Prerequisites

Before running this script, make sure you have:

- Python 3.10 installed on your machine.
- `boto3` and `python-dotenv` library installed. You can install it using `pip install -r requirements.txt`.
- AWS credentials (Access Key ID and Secret Access Key) is defined in the `.env` file.

## Configuration

1. **Set AWS Credentials**: Create a `.env` file in the directory and ensure your AWS credential is defined in the `.env` file

   ```bash
   AWS_ACCESS_KEY_ID="your_access_key_id"
   AWS_SECRET_ACCESS_KEY="your_secret_access_key"
   ```

Replace your_access_key_id and your_secret_access_key with your actual AWS credentials.

Set Data Directory Path: In the script, the data directory path is set default as `./data` replace `data_dir` with the path to the local directory where you want the files to be downloaded.

Specify Bucket and Prefixes: Make sure the bucket_name variable is set to your target AWS S3 bucket name, and update the prefixes list with the desired object key prefixes.

## Usage
Once configured, you can run the script directly from your terminal/cmd/PowerShell:
```bash
python main.py
```

The script will start downloading the files from the specified S3 bucket that match the given prefixes into the specified local directory.