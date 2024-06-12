"""

ADCP Data Parser
Harrison Myers
11/1/2023

"""
import os
import pandas as pd
import numpy as np
from zipfile import ZipFile
# from datetime import datetime

def create_dirs(folder_name="data.zip"):
    """
    Unzips the data folder and creates the directories necessary to run the 
    rest of the script. Changes the working directory, and returns the working
    directory path, and the path of the enclosing, unzipped "data" folder
    containing the datafiles. 
    
    Note: python script must be located in an enclosing folder containing the 
          zipped folder with the data
    
    folder_name - name of zipped folder containing the ADCP .txt datafiles
    """
    # Create relative directory path and change directory
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)
    
    # Make reports folder and unzip reports to this folder
    try:
        os.mkdir("data")
        # loading the temp.zip and creating a zip object 
        with ZipFile(dir_path + "\\" + folder_name) as zObject: 
            # Extracting all the members of the zip into reports
            zObject.extractall(dir_path)
    except:
        pass
    
    # Make a path that points to the data folder where data is stored
    data_dir = dir_path + "\\data"
    
    return dir_path, data_dir

dir_path, data_dir = create_dirs()

def get_gps_data(filename):
    """
    reads a text file of NMEA data and extracts GPS data from the file and 
    returns a pandas dataframe containing UTC time, latitude, longitude, number 
    of satellites, and altitude (m)
    
    filename - name of .txt file to be read
    """
    
    # Create list of columns of gps data
    columns = ['UTC_time', 'Lat', 'Lon', "position_fix", "altitude_m"]
    
    # Create empty dictionary for storing data
    data_dict = {column: [] for column in columns}
    
    # Read the data file line by line and categorize each line into its corresponding list
    with open(filename, 'r') as file:
        for line in file:                                  # for every line in the file
            if line.startswith('$GPGGA'):                  # if GPS data
                data_list = line.strip().split(",")        # split line into list of words
                # Append appropriate data to dictionary
                data_dict[columns[0]].append(data_list[1]) # time
                data_dict[columns[1]].append(data_list[2]) # latitude
                data_dict[columns[2]].append(data_list[4]) # longitude
                data_dict[columns[3]].append(data_list[6]) # position fix (1-worst, 4-best)
                data_dict[columns[4]].append(data_list[9]) # altitude of antenna
    
    # # Create a Pandas DataFrame from the collected data
    df = pd.DataFrame(data_dict)
    
    # Display the DataFrame
    return df

def get_all_data():
    """
    Gets GPS data from all .txt files in the data directory and stores them as
    a dataframe, and saves them as a .csv
    """
    master_df = pd.DataFrame(columns=['UTC_time', 'Lat', 'Lon', "position_fix", "altitude_m"])
    for file in os.listdir(data_dir): # for every file in directory
        point = get_gps_data(data_dir + "\\" + file)
        master_df = master_df._append(point)
    
    for column in master_df.columns:
        master_df[column] = pd.to_numeric(master_df[column]) # convert to numeric datatypes
        if (column == "Lat") or (column == "Lon"):           # convert lat/lon to standard format
            master_df[column] = master_df[column] / 100
        if column == "Lon":
            master_df[column] = master_df[column] * -1
        # if column == "UTC_time":
        #     master_df[column] = pd.to_datetime(master_df[column])
    master_df.dropna(axis=0, inplace=True)                   # drop missing values
    master_df.to_csv(dir_path + "\\" + "gps_data.csv", index=False)  # save as csv
    
    return master_df

survey_data = get_all_data()



