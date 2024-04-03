import os, time, threading, boto3
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path
from parse_signals import *
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
"""
CONFIDENTIAL
__________________
2023 Verisense Health Inc.
All Rights Reserved.
NOTICE:  All information contained herein is, and remains
the property of Verisense Health Incorporated and its suppliers,
if any.  The intellectual and technical concepts contained
herein are proprietary to Verisense Health Incorporated
and its suppliers and may be covered by U.S. and Foreign Patents,
patents in process, and are protected by trade secret or copyright law.
Dissemination of this information or reproduction of this material
is strictly forbidden unless prior written permission is obtained
from Verisense Health Incorporated.
Authors: Lucas Selig <lselig@verisense.net>
"""
sns.set_style("darkgrid")

def plot_signal(combined_out_path, use_datetimes):
    df = pd.read_csv(combined_out_path)
    if("Accel" in combined_out_path):
        fig, axs = plt.subplots(3, 1, figsize = (15, 9), sharex = True)
        if(use_datetimes):
            # axs[0].plot(pd.to_datetime(df.etime, unit = "s"), df.mag)
            axs[0].plot(pd.to_datetime(df.etime, unit = "s"), df.x)
            axs[1].plot(pd.to_datetime(df.etime, unit = "s"), df.y)
            axs[2].plot(pd.to_datetime(df.etime, unit = "s"), df.z)
        else:
            # axs[0].plot(df.etime, df.mag)
            axs[0].plot(df.etime, df.x)
            axs[1].plot(df.etime, df.y)
            axs[2].plot(df.etime, df.z)

        axs[-1].set_xlabel("Time (s)")
        # axs[0].set_ylabel("Acceleration (g)")
        fig.suptitle(combined_out_path)
        plt.show()
    elif("GreenPPG" in combined_out_path):
        have_hr = True
        try:
            df_hr = pd.read_csv(combined_out_path.replace("GreenPPG", "SingleHeartRate"))
        except:
            have_hr = False

        have_my_hr = True
        try:
            my_df_hr = pd.read_csv(combined_out_path.replace("GreenPPG", "GreenPPG_bpm"))
        except:
            have_my_hr = False
        print(f"Have HR: {have_hr}")
        fig, axs = plt.subplots(2, 1, figsize = (15, 9), sharex = True)
        if(use_datetimes):
            if(have_hr):
                axs[0].scatter(pd.to_datetime(df_hr.etime, unit = "s"), df_hr.bpm, color = "black", label = "JC HR")
            if(have_my_hr):
                axs[0].scatter(pd.to_datetime(my_df_hr.etime, unit = "s"), my_df_hr.bpm, color = "green", label = "MY HR")

            axs[1].plot(pd.to_datetime(df.etime, unit = "s"), df.green, color = "green")
        else:
            if(have_hr):
                axs[0].scatter(df_hr.etime, df_hr.bpm, color = "black", label = "JC HR")
            if(have_my_hr):
                axs[0].scatter(my_df_hr.etime, my_df_hr.bpm, color = "green", label = "MY HR")
            axs[1].plot(df.etime, df.green)

        axs[0].set_ylabel("Heart Rate (BPM)")
        axs[0].legend()
        axs[1].set_xlabel("Time (s)")
        axs[1].set_ylabel("Green PPG (a.u.)")
        if(have_hr and have_my_hr):
            fig.suptitle(f"{combined_out_path}\n"
                         f"{np.nanmean(df_hr.bpm): .2f} JC BPM MEAN\n"
                         f"{np.nanmean(my_df_hr.bpm): .2f} MY BPM MEAN")
        plt.show()
    elif("RedPPG" in combined_out_path):
        if(use_datetimes):
            plt.plot(pd.to_datetime(df.etime, unit = "s"), df.red)
        else:
            plt.plot(df.etime, df.red)
        plt.xlabel("Time (s)")
        plt.ylabel("Red PPG (a.u.)")
        plt.title(combined_out_path)
        plt.show()
    elif("SingleHeartRate" in combined_out_path):
        if(use_datetimes):
            plt.plot(pd.to_datetime(df.etime, unit = "s"), df.bpm)
        else:
            plt.plot(df.etime, df.bpm)
        plt.xlabel("Time (s)")
        plt.ylabel("Heart Rate (bpm)")
        plt.title(combined_out_path)
        plt.show()
    elif("Temperature" in combined_out_path):
        if(use_datetimes):
            plt.plot(pd.to_datetime(df.etime, unit = "s"), df.temperature)
        else:
            plt.plot(df.etime, df.temperature)
        plt.xlabel("Time (s)")
        plt.ylabel("Temperature (C)")
        plt.title(combined_out_path)
        plt.show()
    elif("BloodOxygenLevel" in combined_out_path):
        if(use_datetimes):
            plt.scatter(pd.to_datetime(df.etime, unit = "s"), df.spo2)
        else:
            plt.scatter(df.etime, df.spo2)
        plt.xlabel("Time (s)")
        plt.ylabel("Blood Oxygen Level (%)")
        plt.title(combined_out_path)
        plt.show()
    elif("Step" in combined_out_path):
        if(use_datetimes):
            plt.scatter(pd.to_datetime(df.etime, unit = "s"), df.steps)
        else:
            plt.scatter(df.etime, df.steps)

        plt.xlabel("Time (s)")
        plt.ylabel("Steps")
        plt.title(combined_out_path)
        plt.show()
    elif("ECG" in combined_out_path):
        if (use_datetimes):
            plt.plot(pd.to_datetime(df.etime, unit="s"), df.ecg)
        else:
            plt.plot(df.etime, df.ecg)

        plt.xlabel("Time (s)")
        plt.ylabel("ECG (A.U)")
        plt.title(combined_out_path)
        plt.show()
    else:
        raise ValueError("Signal not recognized")
# Function to read a single file from S3 and return a DataFrame
def download_file_from_s3(bucket, key, DATA_START, signal, RAW_DATA_DIR):
    RAW_DATA_DIR = Path(RAW_DATA_DIR)

    date_string = key.split("/")[-1].split("_")[0]
    date_object = datetime.strptime(date_string, "%y%m%d")
    start_date = datetime.strptime(DATA_START,"%y%m%d")
    start_epoch = int(time.mktime(start_date.timetuple()))


    # print(date_object)
    if(signal not in key):
        return None
    elif(date_object < start_date):
        return None
    else:
        AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
        AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
        s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY,
                                 aws_secret_access_key=AWS_SECRET_KEY)

        obj = s3_client.get_object(Bucket=bucket, Key=key)
        file_content = obj["Body"].read()

        user = key.split("/")[1]
        DEVICE = key.split("/")[2]
        fname = key.split("/")[-1]

        # print("Object Key:", key)
        saveloc = Path(f"{RAW_DATA_DIR}/{user}/{DEVICE}/{signal}")
        if (not saveloc.exists()):
            Path(saveloc).mkdir(parents=True, exist_ok=True)
        if (not Path(f"{str(saveloc)}/{fname}").exists()):
            with open(f"{str(saveloc)}/{fname}", 'wb') as file:
                file.write(file_content)
            print(f"{threading.current_thread().name} -- Downloaded: {fname} to {str(saveloc)}")
        else:
            print(f"{threading.current_thread().name} -- Already downloaded: {fname}")

        return f"{str(saveloc)}/{fname}"

def filter_keys(keys, DATA_START, DATA_END, signal):
    filtered_keys = []
    for key in keys:
        date_string = key.split("/")[-1].split("_")[0]
        date_object = datetime.strptime(date_string, "%y%m%d")
        start_date = datetime.strptime(DATA_START,"%y%m%d")
        end_date = datetime.strptime(DATA_END,"%y%m%d")
        if(signal not in key):
            continue
        elif(date_object < start_date):
            continue
        elif(date_object > end_date):
            continue
        else:
            filtered_keys.append(key)
    return filtered_keys

def download_data(PARTICIPANT, DEVICE, RAW_DATA_DIR, DATA_START_GUI, DATA_END_GUI, SELECTED_RAW_SIGNALS):
    load_dotenv()
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
    S3_BUCKET = os.getenv("S3_BUCKET")
    start_time = time.time()

    # SIGNALS = ["Accel", "SingleHeartRate", "GreenPPG", "RedPPG",  "Temperature", "BloodOxygenLevel", "Step"]
    SIGNALS = []
    for k in SELECTED_RAW_SIGNALS:
        if(SELECTED_RAW_SIGNALS[k] == 1):
            SIGNALS.append(k)
    if(len(SIGNALS) == 0):
        print("No signals selected: Exiting")
        return
    PREFIX = f"1/{PARTICIPANT}/{DEVICE}/ParsedFiles/"

    date_obj_start = datetime.strptime(DATA_START_GUI, '%m/%d/%y')
    # Reformat the date to the desired format
    DATA_START = date_obj_start.strftime('%y%m%d')

    date_obj_end = datetime.strptime(DATA_END_GUI, '%m/%d/%y')
    # Reformat the date to the desired format
    DATA_END = date_obj_end.strftime('%y%m%d')

    print(f"Downloading data for {PARTICIPANT} from {DATA_START_GUI} to {DATA_END_GUI}")

    for signal in SIGNALS:
        s3_client = boto3.client('s3',
                                 aws_access_key_id=AWS_ACCESS_KEY,
                                 aws_secret_access_key=AWS_SECRET_KEY)

            # List files in the bucket
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET,
                                          Prefix=PREFIX,
                                          MaxKeys = 2000000)
        files = response["Contents"]
        keys = [file['Key'] for file in files]
        keys = filter_keys(keys, DATA_START, DATA_END, signal)

        # Use ThreadPoolExecutor to parallelize the reading of files
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(download_file_from_s3, S3_BUCKET, key, DATA_START, signal, RAW_DATA_DIR) for key in keys]

        # Continue the process as long as there are more objects
        while response['IsTruncated']:
            response = s3_client.list_objects_v2(
                Bucket=S3_BUCKET,
                Prefix=PREFIX,
                ContinuationToken=response['NextContinuationToken']
            )
            files = response["Contents"]

            keys = [file['Key'] for file in files]
            keys = filter_keys(keys, DATA_START, DATA_END, signal)

            # Use ThreadPoolExecutor to parallelize the reading of files
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(download_file_from_s3, S3_BUCKET, key, DATA_START, signal, RAW_DATA_DIR) for
                           key in keys]

        with ProcessPoolExecutor() as executor:
                # List all CSV files in the directory
                directory = f"{RAW_DATA_DIR}/{PARTICIPANT}/{DEVICE}/{signal}"
                try:
                    os.listdir(directory)
                except:
                    print(f"Directory not found: {directory}")
                    continue

                csv_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.csv')]

                if (signal == "Accel"):
                    dataframes = list(executor.map(parse_accel, csv_files))
                elif (signal == "GreenPPG"):
                    dataframes = list(executor.map(parse_green_ppg, csv_files))
                elif (signal == "RedPPG"):
                    dataframes = list(executor.map(parse_red_ppg, csv_files))
                elif (signal == "SingleHeartRate"):
                    dataframes = list(executor.map(parse_heart_rate, csv_files))
                elif (signal == "Temperature"):
                    dataframes = list(executor.map(parse_temperature, csv_files))
                elif (signal == "BloodOxygenLevel"):
                    dataframes = list(executor.map(parse_spo2, csv_files))
                elif (signal == "Step"):
                    dataframes = list(executor.map(parse_steps, csv_files))
                elif (signal == "ECG"):
                    dataframes = list(executor.map(parse_ecg, csv_files))


        # Concatenate all DataFrames into a single DataFrame
        concatenated_df = pd.concat(dataframes)
        concatenated_df = concatenated_df.sort_values(by = "etime")
        concatenated_df = concatenated_df.drop_duplicates()

        COMBINED_OUT_PATH = f"{RAW_DATA_DIR}/{PARTICIPANT}/{DEVICE}/Parsed"
        OUTFILE = f"{COMBINED_OUT_PATH}/verisense_{signal}.csv"
        print(f"Writing CSV: {OUTFILE}")
        if(not Path(COMBINED_OUT_PATH).exists()):
            Path(COMBINED_OUT_PATH).mkdir(parents=True, exist_ok=True)

        start_date = datetime.strptime(DATA_START, "%y%m%d")
        start_epoch = int(time.mktime(start_date.timetuple()))
        concatenated_df = concatenated_df[concatenated_df.etime > start_epoch]
        concatenated_df.to_csv(OUTFILE, index = False)
        print(f"Wrote CSV: {OUTFILE}")
        elapsed_time = time.time() - start_time
        print(f"The function took {elapsed_time} seconds to complete.")

    return

if __name__ == "__main__":
    download_data()
