# LSGI3315 Group 6's Project - Task 2 Individual Task (30% of total mark of Project)
# Create and Implement a class for outdoor and sport facilities
# Tang Justin Hayse Chi Wing G. - 20016345D

# Import the Package
import pandas as pd
import os
import arcpy

# Setting Current Working Directory (root directory with filtered files and Geodatabase)
arcpy.env.workspace = r"C:\Users\justi\Downloads\LSGI3315_Individual_Group6_20016345D"
os.chdir(arcpy.env.workspace)

# Enable the System to Overwrite the Existing ArcGIS Files
arcpy.env.overwriteOutput = True


class facility:  # Create a Class named "facility"
    def __init__(self):  # Initialization: the Class "facility"
        # List out all csv files of Sports and Outdoor Facilities and define
        csv = ['Badminton_court.csv', 'Basketball_court.csv', 'country_parks.csv', 'fitness_center.csv',
               'other_recreation_sports_facilities.csv', 'parks_gardens.csv', 'sports_grounds.csv', 'swimming_pools.csv']
        for csv_files in csv:
            # Input all csv files
            self.fileInput = csv_files
            # Read the DataFrame
            data_frame = pd.read_csv(self.fileInput, engine='python')
            # Subset the Dataframe and record the attributes of sports and outdoor facilities
            self.df = data_frame[
                ["GMID", "Dataset", "Facility Name", "Address", "District", "Northing", "Easting", "Latitude", "Longitude", "Last Update "]]
            # Create an empty list to store the values from CSV
            self.input_list = []
            # Create a For-loop to scan the rows
            for index, row in data_frame.iterrows():
                # Converting the Pandas Series into list
                data_list = row.tolist()
                # Appending the list into "data_list"
                self.input_list.append(data_list)
            print("The Rows from [", str(csv_files), "] have been stored in the List successfully!")
            self.CSV_To_FeatureClass()

    def CSV_To_FeatureClass(self):   # This Function is to convert the input files into Geodatabase Feature Class
        print("Creating a Feature Class to input point data (Sports and Outdoor Facilities)... ")
        # Create an Empty Feature Class through ArcPy
        self.fc = arcpy.CreateFeatureclass_management("Gp6_20016345D_Task3_v1.gdb", self.fileInput.split(".")[0],
                                                      "POINT", "", "DISABLED", "DISABLED",
                                                      arcpy.SpatialReference(4326))
        # The column in ArcGIS Geodatabase
        column_list = ["GMID", "Dataset", "Facility Name", "Address", "District", "Last Update "]
        # Create a For-loop to add fields into shapefile
        for field in column_list:
            if "Last Update" in field:
                name = field
                field_type = "DATE"
            else:
                name = field
                field_type = "TEXT"
            arcpy.AddField_management(self.fc, name, field_type, field_length=200)
        print("An empty feature class with the required fields is created! Import the point data into Feature Class now...")

        # Fields list of Feature class to insert the data
        featureclass_field_list = ["SHAPE", "GMID", "Dataset", "Facility_Name", "Address", "District", "Last_Update"]
        # Create an ArcPy Data Access cursor to insert values in the feature class
        cursor = arcpy.da.InsertCursor(self.fc, featureclass_field_list)
        # Insert the Point Data into the Feature class
        # Create a For-Loop via Pandas DataFrame
        for index, row in self.df.iterrows():
            # Fetch the preferred information
            shape = arcpy.Point(float(row["Longitude"]), float(row["Latitude"]))
            GMID = row["GMID"]
            dataset = row["Dataset"]
            facility_name = row["Facility Name"]
            address = row["Address"]
            district = row["District"]
            last_update = row["Last Update "]
            # Feature Class Attribute List to insert values
            List_InsertRow = [shape, GMID, dataset, facility_name, address, district, last_update]
            # Inserting new row using the Data Access Cursor
            cursor.insertRow(List_InsertRow)
        print("The Point Data has been inputted into the Feature Class successfully! \n")

    def Nearest_Facility(self):
        arcpy.env.workspace = r"C:\Users\justi\Downloads\LSGI3315_Individual_Group6_20016345D\Gp6_20016345D_Task3_v1.gdb"
        csv = ['Badminton_court', 'Basketball_court', 'country_parks', 'fitness_center',
               'other_recreation_sports_facilities', 'parks_gardens', 'sports_grounds', 'swimming_pools']
        Near = []   # Create an empty list to store the point data for this function
        arcpy.management.Merge(csv, 'merged_fac')   # Merge all point data
        easting = input("Enter the Easting in Hong Kong 1980 coordinate:")  # Input Easting
        northing = input("Enter the Northing in Hong Kong 1980 coordinate:")  # Input Northing
        point = arcpy.Point(float(easting), float(northing))  # Define the Data Type of the Input
        ptGeometry = arcpy.PointGeometry(point, arcpy.SpatialReference(2326))  # Define HK1980 Coordinate System (2326)
        arcpy.CopyFeatures_management(ptGeometry, "inputPoint")
        arcpy.analysis.Near("inputPoint", 'merged_fac', '', '', '', '')
        print(arcpy.GetMessages(), '\n')
        field = ["NEAR_FID", "NEAR_DIST"]
        cursor = (arcpy.da.SearchCursor("inputPoint", field))
        for row in cursor:  # Using for-loop to find the nearest facilities
            Near.append(row[0])
            Near.append(row[1])
        del cursor
        ID = int(Near[0]) - 1
        distance = float(Near[1])
        cursor = arcpy.da.SearchCursor("merged_fac", 'Facility_Name')
        for index, row in enumerate(cursor):
            if index == ID:  # Print the English Name of the nearest facility
                print('The code runs successfully! The English Name of the Nearest Facility is: ' + row[0])
        del cursor
        print('The Distance from the Inputted coordinate to the Sport/Outdoor facility is: ' + str(distance) + ' meters')

    def yesno(self):  # Bonus Part 1: Create a Yes/No Function asking the end-user whether want to try the Bonus Part
        prompt = f'Please type "yes" for the Individual Bonus Part:'
        answer = input(prompt).strip().lower()  # Eliminate the case sensitivity (Allow: YES/Yes/yes/YEs/yeS/yEs/YeS/yES)
        if answer not in ['yes']:
            print(f'Your typed [ {answer} ] is invalid, please type "yes"!')  # print out the wrong answer
            return self.yesno()  # ask the user again if he/she does not type 'yes'
        if answer == 'yes':
            return True  # Go to the Bonus Part
        return False

    def run_yesno(self):
        answer = self.yesno()  # Call the 'yesno' Function
        print(f'Your answer was: {answer}.')  # print out the answer that the end-user typed

    def ArcPy_Search_Cursor(self, fc, address):  # Develop a Search Cursor Function

        with arcpy.da.SearchCursor(fc, address) as user_search_cursor:
            for i in user_search_cursor:
                print("***** Search Result: Name, District and Address:")
                for j in range(len(address)):
                    # display the info in python interface for user
                    fc, address, sql_clause = (None, i, j)  # Set the SQL Clause
                    print((i[j]))  # Print out the result that end-users would like to search
                print("***********************************************************************************************")


if __name__ == "__main__":
    print("***** Mission 1 (Required): Importing the .csv files of Sport and Outdoor Facilities into ArcGIS Pro *****")
    f = facility()
    print("\n")
    print("***** Mission 2 (Required): Finding the Nearest Sport/Outdoor Facility *****")
    f.Nearest_Facility()
    print("\n")
    print("***** Mission 3 (Bonus): Using Search Function to list out the Names of Badminton Court in Hong Kong with Addresses *****")
    f.run_yesno()
    Search_facility = 'Badminton_court.csv'
    Search_facility_address = ['Facility Name', 'District', 'Address']
    f.ArcPy_Search_Cursor(Search_facility, Search_facility_address)
    print("This is the END of LSGI3315 Group 6's Individual Part: Tang Justin Hayse Chi Wing G. (20016345D)")
    print("Thank you for running the Python Script!")
