import requests
import time

# Configuration
base_url = "https://vts-url"  # Replace with the actual VTS URL
email = "user@example.com"  # Replace with your login email
password = "password123"  # Replace with your login password
start_date = "2024-11-01"  # Replace with your desired start date
end_date = "2024-11-05"  # Replace with your desired end date
email_for_data = "email@email.com"  # Replace with the email to receive the data
downloaded_filename = "downloaded_file.tar"  # Replace with the name of the downloaded file - keep the .tar extension


def authenticate():
    auth_url = f"{base_url}/api/auth/sign_in"
    payload = {"Login": email, "Password": password}
    response = requests.post(auth_url, json=payload)
    response_data = response.json()

    if response.status_code == 200 and response_data.get("accesToken"):
        print("Authentication successful!")
        return response_data["accesToken"]
    else:
        print("Authentication failed:", response_data.get("error"))
        return None


def request_data_download(token):
    download_url = f"{base_url}/api/participants/get_concatenated_data"
    payload = {
        "Token": token,
        "StartDate": start_date,
        "EndDate": end_date,
        "ParticipantIdentifier": "",
        "DataType": "",
        "Email": email_for_data,
    }
    response = requests.post(download_url, json=payload)
    response_data = response.json()

    if response.status_code == 200 and response_data.get("isSuccess"):
        request_id = response_data["entity"]["requestId"]
        print("Data download request initiated. Request ID:", request_id)
        return request_id
    else:
        print("Data download request failed:", response_data.get("error"))
        return None


def check_download_status(token, request_id):
    status_url = f"{base_url}/api/participants/get_concatenated_data_request_status"
    payload = {"Token": token, "RequestUUID": request_id}
    while True:
        response = requests.post(status_url, json=payload)
        response_data = response.json()
        if response.status_code == 200 and response_data.get("isSuccess"):
            status = response_data["entity"]["status"]
            if status == "Completed":
                download_url = response_data["entity"]["presignedUrl"]
                print("Data is ready for download.")
                return download_url
            elif status == "Failed":
                print(
                    "Data request failed. Please try re-running the script. If the issue persists, contact support."
                )
                return None
            else:
                print("Request status:", status, "- Checking again in 5 seconds...")
                time.sleep(5)
        else:
            print("Error checking request status:", response_data.get("error"))
            return None


def download_file(download_url):
    response = requests.get(download_url, stream=True)
    if response.status_code == 200:
        total_size = int(response.headers.get("content-length", 0))
        total_size_mb = total_size / (1024 * 1024)  # Convert bytes to megabytes
        file_name = downloaded_filename
        chunk_size = 1024  # 1 KB per chunk
        progress = 0

        print(f"Total file size: {total_size_mb:.2f} MB")

        with open(file_name, "wb") as file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:  # Filter out keep-alive new chunks
                    file.write(chunk)
                    progress += len(chunk)
                    percentage = (progress / total_size) * 100
                    downloaded_mb = progress / (1024 * 1024)  # Convert bytes to MB
                    print(
                        f"\rDownloading... {downloaded_mb:.2f} MB / {total_size_mb:.2f} MB ({percentage:.2f}%)",
                        end="",
                    )

        print(f"\nData downloaded successfully as {file_name}")
    else:
        print("Failed to download the file. Status code:", response.status_code)


# Execution
token = authenticate()
if token:
    request_id = request_data_download(token)
    if request_id:
        time.sleep(2)
        download_url = check_download_status(token, request_id)
        if download_url:
            download_file(download_url)
