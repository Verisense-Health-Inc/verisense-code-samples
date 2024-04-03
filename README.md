
<<<<<<< HEAD
=======
- Download and install **PyCharm** from the [official website](https://www.jetbrains.com/pycharm/download/).
- Download and install **Git** from the [official website](https://git-scm.com/downloads).

## Step 2: Download Python 3.10 Installer

1. Visit the official Python website at [https://www.python.org/downloads/release/python-3100/](https://www.python.org/downloads/release/python-3100/)
2. Scroll down to the **Files** section.
3. Under "Windows installer (64-bit)" choose the installer that matches your system. (Most modern Windows systems are 64-bit but you can choose the 32-bit installer if you have an older system.)
4. Click on the download link to start the download.
5. Once the installer executable (.exe) is downloaded, locate it in your Downloads folder or the location where you saved it.
6. Double-click the installer to run it.
7. In the Python installer window, make sure to check the box that says "Add Python 3.10 to PATH." (This is important to easily run Python from the command prompt.)
8. Click the "Install Now" button to start the installation process.

## Step 3: Clone the GitHub Repository

Open your terminal or command prompt and run the following command to clone the Verisense Health GitHub repository:

```bash
https://github.com/Verisense-Health-Inc/aws-s3-file-downloader.git
```

## Step 4: Open the Repository in PyCharm

1. Open PyCharm.
2. Go to **File > Open** and navigate to the `aws-s3-file-downloader` directory that you just cloned. Click "Open."
3. PyCharm may ask you to "Attach" and "Trust Project." Confirm these actions.

## Step 5: Install Required Dependencies

In the PyCharm interface:

1. Make sure you have the `aws-s3-file-downloader` project selected in the left panel.
2. Choose **View > Tool Windows > Terminal** to open a terminal window within PyCharm.
3. Run the following command to install project requirements:

```bash
pip install -r requirements.txt
```

## Step 6: Create and Configure the .env and Script Parameters

1. Right-click on the `aws-s3-file-downloader` project in the left panel.
2. Choose **New > File** and name it `.env` (without quotes).
3. Inside the `.env` file, add the following lines and replace them with your temporary or read-only access keys from the bitwarden link and configure the parameters according to your desired settings. Here's an example configuration:

```
AWS_ACCESS_KEY="AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
S3_BUCKET = 'verisense-1d2677bd-c22f-49ec-b4db-1b4c1ee90e5e'
```

## Step 7: Run the verisense_datafetch.py Script

1. In PyCharm, make sure the above script is open.
2. Locate the "Run" button in the PyCharm interface (typically a green triangle or "Play" button) and press it.
3. This will open a GUI application.

<img width="804" alt="Screen Shot 2024-04-03 at 11 44 07 AM" src="https://github.com/Verisense-Health-Inc/aws-s3-file-downloader/assets/162383276/bbe20c97-3913-415a-adf6-53da2105da70">

4. For participant ID enter the participant ID.
5. For device ID enter the 12 character bluetooth ID.
6. For the output folder enter a valid folder on your computer where you wish to have the data downloaded to (no slash at the end).
7. For data begin and data end use the dropdowns (may have to double click) to select the date range for your data.
8. Use the checkboxes to select the signals you are interested in downloading.
## Step 8: View the Output

After running the script, you should see concatenated data for various signals in your specified directory. You can access and analyze the results from this directory.

## Step 9: Data Formats

Here is a quick explanation of the data

### Acceleration
| Column | Unit | Notes |
| --- | --- | --- |
| etime | seconds | Timestamp of the data point in seconds |
| x | g | x-axis of acceleration |
| y | g | y-axis of acceleration |
| z | g | z-axis of acceleration |

### Green PPG
| Column | Unit | Notes |
| --- | --- | --- |
| etime | seconds | Timestamp of the data point in seconds |
| green | A.U | green PPG |

### Red PPG
| Column | Unit | Notes |
| --- | --- | --- |
| etime | seconds | Timestamp of the data point in seconds |
| red | A.U | red PPG |

### Temperature
| Column | Unit | Notes |
| --- | --- | --- |
| etime | seconds | Timestamp of the data point in seconds |
| temperature | C | wrist temperature |

### Heart Rate
| Column | Unit | Notes |
| --- | --- | --- |
| etime | seconds | Timestamp of the data point in seconds |
| bpm | beats per minute | heart rate |

### Blood Oxygen Level
| Column | Unit | Notes |
| --- | --- | --- |
| etime | seconds | Timestamp of the data point in seconds |
| spo2 | % | blood oxygen level |

**That's it! You've successfully configured and run the script in PyCharm for the Verisense Health's dsci_algorithms_python repository.**
>>>>>>> 3fa9cdd (Update README.md)
