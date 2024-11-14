# Data Download Script

This script is a Python utility designed to authenticate with a VTS API, request data, and download the resulting file. The script includes functions for authentication, data request, status checking, and downloading the file.

## Requirements

- Python 3.x
- `requests` library

To install the required library, run:

```sh
pip install requests
```

## Configuration

Before running the script, make sure to configure the following:

- `base_url`: Replace with the actual VTS URL.
- `email`: Your VTS operator or site admin login email.
- `password`: Your VTS operator or site admin login password.
- `start_date`: Desired start date for data extraction (e.g., "2024-11-01").
- `end_date`: Desired end date for data extraction (e.g., "2024-11-05").
- `email_for_data`: The email address to receive the data notification.

## Script Overview

### Functions

1. **`authenticate()`**
   - Authenticates with the VTS API.
   - Returns an access token if successful.

2. **`request_data_download(token)`**
   - Requests data download from the API for a specified date range.
   - Returns a request ID if successful.

3. **`check_download_status(token, request_id)`**
   - Checks the status of the data download request.
   - If the request is completed, it returns a presigned download URL.

4. **`download_file(download_url)`**
   - Downloads the data file from the provided URL.

## How to Run the Script

1. Update the configuration parameters with appropriate values.
2. Run the script:

   ```sh
   python data_download.py
   ```

The script performs the following tasks sequentially:
1. **Authentication**: It authenticates with the VTS API using your login credentials.
2. **Data Download Request**: It initiates a data download request for the specified time range.
3. **Check Download Status**: It periodically checks the status of your data download request.
4. **Download Data**: Once the data is ready, the script will download the file.

## Script Workflow
- **`authenticate()`**: Authenticates with the API and returns an access token.
- **`request_data_download(token)`**: Requests a data download, using the token for authentication.
- **`check_download_status(token, request_id)`**: Continuously checks the status of the download request until it completes.
- **`download_file(download_url)`**: Downloads the data using a pre-signed URL.

## Important Notes
- Make sure your `base_url`, `email`, and `password` are correct to successfully authenticate with the VTS API.
- The script checks the download request status every 5 seconds until the data is ready.
- This is a basic example of handling API requests and responses. Depending on the API's response, you may need to adjust the script to handle different error messages or response formats.

## Disclaimer
This script contains sensitive information, such as passwords and tokens. Make sure to keep it secure and avoid sharing it publicly. Consider using environment variables or a configuration file for sensitive data to enhance security.
