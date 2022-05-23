# LSGI3315 Group 6's Project - Task 1: Data Cleaning
# Group mate 1: Wei Jun, Kenny - 20084091D
# Group mate 2: Tang Justin Hayse Chi Wing G. - 20016345D
import pandas as pd
import os

print("========================================== Task 1: Data Cleaning ===========================================")
data_folder = r"C:\Users\justi\Downloads\LSGI3315_Gp6_20016345D"  # working directory containing .csv files is set
os.chdir(data_folder)  # Changing the working directory
files = os.listdir(os.getcwd())  # receive all .csv files inside the folder
files = list(filter(lambda f: f.endswith('.csv'), files))  # find all ".csv" files in folder

out_path = r"C:\Users\justi\Downloads\LSGI3315_Gp6_Output_Files"  # Path to output directory

for file in files:  # Create a for-loop to loop through the data in .csv file
    df = pd.read_csv(file)  # Reading .csv files using pandas dataframe
    # subset the information which are kept
    df_subset = df[["Dataset", "Facility Name", "Address", "District", "Northing", "Easting", "Latitude", "Longitude"]]
    df_subset.to_csv(out_path + file)  # Save the data frames as .csv file as output
print("==================================== Task 1: Data Cleaning is completed! ====================================")
