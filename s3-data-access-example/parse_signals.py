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

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from dateutil import parser

sns.set_style("darkgrid")
def parse_steps(infile):
    # passing a df
    if (not isinstance(infile, str)):
        df = infile
        pass
    # passing a filename
    else:
        try:
            df = pd.read_csv(infile, skiprows=9)
        except:
            return None
    df.columns = ["etime", "steps", "calories", "distance", "detail_step"]
    df = df.drop(["detail_step"], axis = 1)
    df = df[1:]
    df["etime"] =  [parser.parse(x).timestamp() for x in df.etime]
    df = df.sort_values(by="etime")
    return df
def parse_spo2(infile):
    # passing a df
    if (not isinstance(infile, str)):
        df = infile
        pass
    # passing a filename
    else:
        try:
            df = pd.read_csv(infile, skiprows=9)
        except:
            return None
    df.columns = ["etime", "spo2"]
    df = df[1:]
    df["etime"] =  [parser.parse(x).timestamp() for x in df.etime]
    df = df.sort_values(by="etime")
    return df

def parse_temperature(infile):
    # passing a df
    if (not isinstance(infile, str)):
        df = infile
        pass
    # passing a filename
    else:
        try:
            df = pd.read_csv(infile, skiprows=9)
        except:
            return None
    df.columns = ["etime", "temperature"]
    try:
        df["etime"] =  [parser.parse(x).timestamp() for x in df.etime]
    except:
        return None
    df = df.sort_values(by="etime")
    return df

def parse_ecg(infile):
    # df = pd.read_csv(infile, skiprows=8)
    # passing a df
    if (not isinstance(infile, str)):
        df = infile
        pass
    # passing a filename
    else:
        try:
            df = pd.read_csv(infile, skiprows=9)
        except:
            return None
    df.columns = ["etime", "hrv", "hr", "mood", "ecg"]
    vals = []
    df = df[1:]
    for i in range(df.shape[0]):
        str_row = df.iloc[i].ecg
        for val in str_row.split(","):
            if(val != ""):
                vals.append(int(val))

    start = read_line(infile, 4)
    end = read_line(infile, 5)
    start_etime = int(start.split("\n")[0].split("=")[-1]) / 1000
    end_etime = int(end.split("\n")[0].split("=")[-1]) / 1000
    etime = np.linspace(start_etime, end_etime, num = len(vals))
    df = pd.DataFrame({"etime": etime,
                       "ecg": vals})
    df = df.sort_values(by="etime")
    return df
def read_line(infile, linei):
    with open(infile, "r") as f:
        for i, line in enumerate(f):
            if(i == linei - 1):
                return line
    return None
def parse_accel(infile):
    if(not isinstance(infile, str)):
        df = infile
        pass
    else:
        try:
            df = pd.read_csv(infile, skiprows=9)
        except:
            return None
    # df = infile
    print(f"Working on accel df with shape: {df.shape}")
    df.columns = ["etime", "x", "y", "z"]
    df["x"] = (df["x"] / 9.8)
    df["y"] = (df["y"] / 9.8)
    df["z"] = (df["z"] / 9.8)
    df["etime"] = df["etime"] / 1000
    return df
def parse_green_ppg(infile, show_plot = False):
    # passing a df
    if (not isinstance(infile, str)):
        df = infile
        pass
    # passing a filename
    else:
        try:
            df = pd.read_csv(infile, skiprows=9)
        except:
            return None
    # df = pd.read_csv(infile, skiprows=9)
    df.columns = ["etime", "green"]
    df["etime"] = df["etime"] / 1000
    df = df.sort_values(by="etime")
    if(show_plot):
        plt.plot(df.etime, df.green)
        plt.xlabel("Time (s)")
        plt.ylabel("Green PPG (a.u.)")
        plt.title(infile.split("/")[-1])
        plt.show()
    return df
def parse_red_ppg(infile, show_plot = False):
    # print(infile)
    # passing a df
    if (not isinstance(infile, str)):
        df = infile
        pass
    # passing a filename
    else:
        try:
            df = pd.read_csv(infile, skiprows=9)
        except:
            return None
    # df = pd.read_csv(infile, skiprows=9)
    df.columns = ["etime", "red"]
    df["etime"] = df["etime"] / 1000
    df = df.sort_values(by="etime")
    if (show_plot):
        plt.plot(df.etime, df.red)
        plt.xlabel("Time (s)")
        plt.ylabel("Red PPG (a.u.)")
        plt.title(infile.split("/")[-1])
        plt.show()
    return df


def parse_heart_rate(infile):
    # df = pd.read_csv(infile, skiprows=9)
    # passing a df
    if (not isinstance(infile, str)):
        df = infile
        pass
    # passing a filename
    else:
        try:
            df = pd.read_csv(infile, skiprows=9)
        except:
            return None
    df.columns = ["etime", "bpm"]
    etimes = []
    bpms = []
    for i, x in enumerate(df.etime.values):
        # print(parser.parse(x).timestamp())
        # print(int(str(df.bpm.values[i]).split(" ")[0]))
        etimes.append(parser.parse(x).timestamp())
        bpms.append(int(str(df.bpm.values[i]).split(" ")[0]))

    df = pd.DataFrame({"etime": etimes, "bpm": bpms})
    df = df.sort_values(by="etime")
    return df

