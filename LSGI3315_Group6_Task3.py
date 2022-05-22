# LSGI3315 Group 6's Project - Task 3 Group Task (70% of total mark of Project)
# Task 3: Create Python Scripts and Modules to analyze the Spatial Distribution of Sports and Outdoor Facilities in Hong Kong
# Group mate 1: Wei Jun, Kenny - 20084091D
# Group mate 2: Tang Justin Hayse Chi Wing G. - 20016345D

# Import the Python Package/ Module
import arcpy
import os
import random
import string
from arcpy.sa import *
from itertools import combinations

# Overwrite the arcpy environment
arcpy.env.overwriteOutput = True


# This function is to return the random letter in Python
def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))


# This function is to set up the coordinate system in ArcGIS Environment
def project_data(in_features):
    desc = arcpy.Describe(in_features)
    spatial_reference = desc.spatialReference
    project_shp = ''
    if spatial_reference.type == u'Geographic':
        # Spherical Mercator projection coordinate system (ESPG3857) is selected.
        out_coordinate_system = arcpy.SpatialReference(3857)  # input ESPG3857
        project_shp = random_char(5)  # generate random string of 5 characters
        arcpy.Project_management(in_features, project_shp, out_coordinate_system)
    if project_shp != '':
        return project_shp
    else:
        return in_features


'''
==========================================Kernel Density Estimation=====================================================
This is used to conducted the kernel density estimation of the sports and outdoor facilities.
feature_type: one of the sports and outdoor facilities
========================================================================================================================
'''


# Perform kernel density estimation
def Kernel_Density(facility_type):
    input_feature = facility_type  # define the input feature class
    population = 'None'  # NONE is used by default in the population field
    inBarriers = base_path + "\\Raw_Data\\hk map\\Hong_Kong_18_Districts-shp\\HKDistrict18.shp"
    # perform Kernel Density (Spatial Analyst)
    outKernelDensity = arcpy.sa.KernelDensity(input_feature, population, "", "", "", "", "", inBarriers)
    # Save the output feature class as facility name + _KernelDensity
    outKernelDensity.save("task_one_kernelRasterResult")
    # tell user the analysis process finished
    print('\nFinish calculate %s density' % facility_type)


'''
=================Task 3.1 Spatial Distribution of Different types of Sports and Outdoor Facilities======================
This is used to explore the spatial distribution of various sports and outdoor facilities via ArcPy
searching_distance = input of searching distance
cell_interval = cell interval for fishnet
========================================================================================================================
'''


def Different_SpatialDistribution_Facilities(searching_distance, cell_interval):
    inputted_distance = searching_distance  # Save the user input of searching distance
    inputted_interval = cell_interval  # Save the user input of cell interval for fishnet
    temp_list = []  # Create an Empty List

    #  Using HK1980 Grid Coordinate System to create a Fishnet is easier because it use meter as the unit
    spatial_reference = arcpy.SpatialReference(2326)  # EPSG 2326 = HK1980 Grid Coordinate System
    arcpy.env.outputCoordinateSystem = spatial_reference  # set this coordinate system temporarily

    # Create a Fishnet of rectangular cells by inputting the essential parameters
    arcpy.management.CreateFishnet("fishnet", '801010.096208300 801656.030632100', '801010.096208300 801666.030632100',
                                   inputted_interval, inputted_interval, '', '', '863615.312086720 846943.245240580',
                                   'LABELS', '', '')
    arcpy.Delete_management("fishnet")

    # Input the data from the List
    types_of_facilities = ['Badminton_court', 'Basketball_court', 'country_parks', 'fitness_center',
                           'parks_gardens', 'sports_grounds', 'swimming_pools', 'other_recreation_sports_facilities']

    # Create a For-loop for looping all types of sports and outdoor facilities
    for index, value in enumerate(types_of_facilities):
        # Define the output coordinate system again. To be remarked, the coordinate system will be changed at the end.
        arcpy.env.outputCoordinateSystem = spatial_reference

        # Use the Spatial Join Function to let the points import into the defined width of cells in fishnet
        arcpy.analysis.SpatialJoin("fishnet_label", str(value),
                                   "fishnet_label_temporary" + str(index), 'JOIN_ONE_TO_MANY',
                                   'KEEP_COMMON', '', 'WITHIN_A_DISTANCE', str(inputted_distance) + ' meters')
        arcpy.DeleteIdentical_management("fishnet_label_temporary" + str(index), "TARGET_FID")
        temp_list.append("fishnet_label_temporary" + str(index))  # Append the temporary output

    arcpy.management.Merge(temp_list, 'temp_merged')  # Merge the temporary output

    # Using ArcPy Spatial Join Function to let the point data import into the specific width of cells
    arcpy.analysis.SpatialJoin("fishnet_label", 'temp_merged', "fishnet_final", 'JOIN_ONE_TO_ONE', 'KEEP_COMMON', '',
                               'INTERSECT', '', '')

    # Remove the cells located in the sea or irrelevant areas in Hong Kong
    arcpy.analysis.Clip("fishnet_final", HK_shapefile, "clipped_fishnet_final")


'''
============================================Task 3.2-3.3:Buffer analysis================================================
Buffer analysis for determining the service coverage.
in_features：facility data such as sport centers.
out_feature_class：output result.
buffer_distance：user-defined service distance.
dissolve_option:Whether the overlaps among buffers will be removed. 
========================================================================================================================
'''


# Task3.2 (1): Conduct the Simple Buffer Analysis for a type of Sports and Outdoor Facility
def buffer_analysis_One(in_features, out_feature_class, buffer_distance, dissolve_option=None):
    try:
        handle_in_features = project_data(in_features)
        # Conducting the buffer analysis and the same set of values in their Dissolve Field(s) will be dissolved together.
        arcpy.Buffer_analysis(handle_in_features, out_feature_class, buffer_distance, dissolve_option=dissolve_option)
        arcpy.Delete_management(handle_in_features)
    except Exception as result:
        raise Exception(result)


# Task3.2 (2): Conduct the Intersect Analysis for the Buffers which are currently generated
def Intersect_analysis_and_calc_param(target_features, intersect_features):
    try:
        # Processing the data by using intersect tool,
        # thus the surface areas which are outside the corresponding district will be removed.
        handle_target_features = project_data(target_features)
        handle_intersect_features = project_data(intersect_features)
        # Save the target and intersect features in the "inFeature"
        inFeatures = [handle_target_features, handle_intersect_features]
        # Create the output name from the intersect analysis
        intersect_output = "task_two_intersect_result"
        # Conduct the intersect analysis
        arcpy.Intersect_analysis(inFeatures, intersect_output)
        print("The Intersect Analysis is completed.")
        rDict_double = {}

        # Compute the percentage by surface area(buffer)/District area
        fields = ["CNAME_S", "SHAPE@AREA"]  # Create a field contains name and the area of buffers
        with arcpy.da.SearchCursor(handle_target_features, fields) as cursor:
            #  Create a Nested For-loop to compute the total area of buffers
            for row in cursor:  # Create a First for-loop to scan the attribute table
                xzqmc = row[0]
                total_area = 0
                # Select the information from the attribute
                temp_layer = arcpy.SelectLayerByAttribute_management(intersect_output, "NEW_SELECTION",
                                                                     '"CNAME_S" = ' + "'" + xzqmc + "'")
                arcpy.CopyFeatures_management(temp_layer, xzqmc + "_tempLayer")
                # Find the "SHAPE@AREA" from the attribute
                with arcpy.da.SearchCursor(temp_layer, ["SHAPE@AREA"]) as cursor2:
                    for row2 in cursor2:  # Create a second for-loop to increment the total area
                        total_area += row2[0]  # add the total area of buffers

                # The formula to compute the surface coverage
                rDict_double[xzqmc] = (total_area / row[1]) * 100
                arcpy.Delete_management(xzqmc + "_tempLayer")
        arcpy.Delete_management(handle_target_features)
        arcpy.Delete_management(handle_intersect_features)
        print("Buffer Analysis is completed.")
        return rDict_double  # return the output of the surface coverage

    except Exception as result:
        raise Exception(result)


# Task3.2 (3): Copy the results to The Shapefile of Hong Kong 18 Districts.
def copyResultToXzq(new_field_name, source_layer, result_layer, dict):
    try:
        arcpy.CopyFeatures_management(source_layer, result_layer)
        # Add the output surface coverage to the new field "Surface_percentage"
        arcpy.AddField_management(result_layer, new_field_name, "DOUBLE", 2, field_alias="Surface_percentage(%)")
        with arcpy.da.UpdateCursor(result_layer, ["CNAME_S", new_field_name]) as cursor:
            # Create a for loop to loop the surface percentage to all districts
            for row in cursor:
                layer_xzqmc = str(row[0])
                row[1] = float(dict[layer_xzqmc])
                cursor.updateRow(row)  # update the row
    except Exception as result:
        raise Exception(result)


'''
===========================Task 3.4:Exploring the Coverage of Multiple Sports/Outdoor Facilities =======================
These functions are to find the good coverage of three or above sports and outdoor facilities
input_buffer distance = customized buffer radius from end-user 
feature class = select one sport facility
searching_distance = customized buffer radius from end-user 
input_facility_list = input three or above sport facilities
========================================================================================================================
'''


def Buffer_Analysis_for_Multiple_Facilites(input_buffer_distance, feature_class):
    arcpy.Buffer_analysis(feature_class, str(feature_class) + "_buffer", str(input_buffer_distance) + " Meters")
    arcpy.analysis.Union(str(feature_class) + "_buffer", str(feature_class) + "_union")
    arcpy.MultipartToSinglepart_management(str(feature_class) + "_union", str(feature_class) + "_multipartToSinglepart")
    arcpy.Delete_management(str(feature_class) + "_union")
    arcpy.SpatialJoin_analysis(str(feature_class) + "_multipartToSinglepart",
                               str(feature_class) + "_multipartToSinglepart", str(feature_class) + "_join_raw", "", "",
                               "", "ARE_IDENTICAL_TO", "", "")
    arcpy.Delete_management(str(feature_class) + "_multipartToSinglepart")

    arcpy.Clip_analysis(str(feature_class) + "_join_raw", HK_shapefile, str(feature_class) + "_join")

    arcpy.MakeFeatureLayer_management(str(feature_class) + "_join", str(feature_class) + "_join_lyr")
    # getting maximum values from the Join_Count field of the layer
    listname = []
    cursor = arcpy.da.SearchCursor(str(feature_class) + "_join_lyr", "Join_Count")
    #  Looping and appending values in the list
    for row in cursor:
        listname.append(int(row[0]))
    del cursor
    max_Join_Count = max(listname)
    arcpy.SelectLayerByAttribute_management(str(feature_class) + "_join_lyr", "NEW_SELECTION", ' "Join_Count" >= 3 ')
    arcpy.CopyFeatures_management(str(feature_class) + "_join_lyr", str(feature_class) + "_join_filtered")
    arcpy.Delete_management(str(feature_class) + "_join_lyr")


# Task 3.4: Which Areas have a Good Coverage of three types of above sports and facilities in Hong Kong?
def Three_or_above_Facilities(input_search_radius, input_facility_list):
    input_buffer_distance = input_search_radius
    input_buffer_distance = int(input_buffer_distance)  # set as integer data type
    types_of_facilities = input_facility_list

    print("Start to conduct the buffer analysis of types of sports and outdoor facilities.")
    # Create a for loop to loop through the point data for creating buffers
    for feature_class_in_list in types_of_facilities:
        Buffer_Analysis_for_Multiple_Facilites(input_buffer_distance, feature_class_in_list)  # Call Function
    print("The types of Buffer analysis (Called Function) are completed!")
    names_list = []  # Create an empty name list

    # Create a for loop to loop through the filtered buffers
    for temp_fac in types_of_facilities:
        name = temp_fac + "_join_filtered"  # add the "_filtered"
        names_list.append(name)  # Append the results

    three_or_above_facilities_list = []  # Create an empty list for three and above facilities
    for comb in combinations(names_list, 3):  # Default three types of facilities
        un_list = list(comb)  # record the for loop
        three_or_above_facilities_list.append(un_list)  # Append the result

    print("Start to conduct the buffer analysis of three types of sports and outdoor facilities.")
    individual_names_list = []  # Create a list for three or above types of feature coverage
    i = 1
    # Create a for loop for
    for combination in three_or_above_facilities_list:
        arcpy.Intersect_analysis(combination, "multiFeatureCoverageArea_" + str(i), "ONLY_FID")
        individual_names_list.append("multiFeatureCoverageArea_" + str(i))
        i = i + 1
    # Merge the three coverages of buffer into one merged feature coverage
    arcpy.management.Merge(individual_names_list, "multiFeatureCoverage")
    # Copy the merged feature to the ArcGIS Geodatabase
    arcpy.CopyFeatures_management(base_path + "\\Raw_Data\\Facility_data.gdb" + "\\multiFeatureCoverage",
                                  temp_gdb + "\\multiFeatureCoverage")
    i = 1
    # Create a for loop to remove the excess files
    for combination in three_or_above_facilities_list:
        arcpy.Delete_management("multiFeatureCoverageArea_" + str(i))
        arcpy.Delete_management("multiFeatureCoverageArea_clip" + str(i))
        i = i + 1
    print("The Coverage analysis of the three or above types of Sports and Outdoor Facilities is completed.")
    print("Please open the ArcGIS Geodatabase in ArcGIS Pro to check the Degree of Coverage.")


'''
======================================Task 3.5:Transportation accessibility=============================================
Transportation accessibility analysis.
road_layer：road network data.
search_distance：user-defined distance for searching facilities.
facility_layer：Facility data.
analysis_result_layer: output result.
========================================================================================================================
'''


# Task 3.5 (Bonus) Evaluating the Transportation Accessibility of one type of Sports/Outdoor Facilities
def traffic_access_analysis(road_layer, search_distance, facility_layer, analysis_result_layer):
    print("Searching the features of Sports and Outdoor Facilities...")
    try:
        # Check the coordinate system of the shapefile(geodesic coordinate system/projected coordinate system)
        desc = arcpy.Describe(road_layer)
        spatial_reference = desc.spatialReference  # Determine the Coordinate System

        # select the features within the user-defined distance
        if spatial_reference.type == u'Geographic':
            # use geodesic distance for the geodesic coordinate system
            temp_layer = arcpy.SelectLayerByLocation_management(facility_layer,
                                                                overlap_type='WITHIN_A_DISTANCE_GEODESIC',
                                                                select_features=road_layer,
                                                                search_distance=search_distance)
        else:
            # use projected distance for the projected coordinate system
            temp_layer = arcpy.SelectLayerByLocation_management(facility_layer, overlap_type='WITHIN_A_DISTANCE',
                                                                select_features=road_layer,
                                                                search_distance=search_distance)

        # Output the selected features to the temporary Geodatabase
        arcpy.CopyFeatures_management(temp_layer, analysis_result_layer)
        print("Searching features completed.")

        # Compute the coverage rate of the road network
        total_count = arcpy.GetCount_management(facility_layer)  # total number of a type of facility
        within_count = arcpy.GetCount_management(analysis_result_layer)  # number of the facility within search radius
        result = str(
            round(round(int(within_count[0]) / int(total_count[0]), 2) * 100)) + "%"  # formula of coverage rate
        return result
    except Exception as result:
        raise Exception(result)


if __name__ == '__main__':  # Main Function
    try:
        # Generate a temporary GDB for storing the final results from tasks 1 to 4.
        # If there is already a GDB, the old GDB will be deleted and a new GDB will be created.
        # Get the current project location.
        base_path = os.path.dirname(os.path.realpath(__file__))  # A smart way to create the directory
        temp_gdb = base_path + "\\fGDB.gdb"  # Directory of Temporary ArcGIS Geodatabase
        HK_shapefile = base_path + "\\Raw_Data\\hk map\\Hong_Kong_18_Districts-shp\\HKDistrict18.shp"  # Directory of Hong Kong Shapefile
        if arcpy.Exists(temp_gdb):
            arcpy.Delete_management(temp_gdb)
        if not os.path.exists(os.path.dirname(temp_gdb)):
            os.mkdir(os.path.dirname(temp_gdb))
        arcpy.CreateFileGDB_management(os.path.dirname(temp_gdb), os.path.basename(temp_gdb), "10.0")
        arcpy.env.workspace = temp_gdb
        print(
            "======================================== LSGI3315 (GIS Engineering) Group 6 Group Project  ========================================")
        print("")
        print(
            "================================================ Testing：Kernel Density Estimation ================================================")
        kernel_in_features = base_path + "\\Raw_Data\\Facility data\\Badminton_court.shp"
        Kernel_Density(kernel_in_features)
        print("The Kernel Density Output is already saved to the ArcGIS Geodatabase：" + os.path.join(temp_gdb))
        print("")

        print(
            "====================== Task 3.1:Spatial Distribution of Different Types of Sports Facilities =======================================")
        arcpy.env.workspace = base_path + "\\Raw_Data\\Facility_data.gdb"
        Different_SpatialDistribution_Facilities(800, 500)  # (searching distance, cell_interval) of Fishnet
        print(
            "The Spatial Distribution of Different Types of Sports Facilities (Fishnet) is already saved to the ArcGIS Geodatabase：" + os.path.join(
                temp_gdb))
        print("")

        print(
            "========================== Task 3.2: One type of Sport Facilities within reasonable walking distance ===============================")
        # Customization: Type the name of the shapefile of sports facilities
        task_two_buffer_in_features = base_path + "\\Raw_Data\\Facility data\\Badminton_court.shp"
        task_two_buffer_out_feature_class = "task_three_bufferResult"
        task_two_buffer_distance = "500 Meters"  # Customization: The Buffer Radius
        buffer_analysis_One(task_two_buffer_in_features, task_two_buffer_out_feature_class,
                            task_two_buffer_distance, dissolve_option='ALL')
        print(" The reasonable walking distance assessment is completed, the result is saved to：" + os.path.join(temp_gdb,
                                                                                        task_two_buffer_out_feature_class))
        print("")

        print(
            "========================== Task 3.3: Good and Bad coverage of one type of the Sports Facilities ====================================")
        target_analysis_layer = base_path + "\\Raw_Data\\hk map\\Hong_Kong_18_Districts-shp\\HKDistrict18.shp"
        rDict_double = Intersect_analysis_and_calc_param(target_analysis_layer,
                                                         task_two_buffer_out_feature_class)
        copyResultToXzq("percent", target_analysis_layer, "Hong_Kong", rDict_double)
        print("Good and Bad coverage of one Sports Facilities is completed.")
        print(
            "The Service percentage is saved to the Shapefile Hong Kong 18 Districts , the file path is: " + os.path.join(
                temp_gdb,
                "Hong_Kong"))
        print("")

        print(
            "======================= Task 3.4: Good and Bad coverage of three or above types of the Sports Facilities ===========================")
        arcpy.env.workspace = base_path + "\\Raw_Data\\Facility_data.gdb"
        task3_three_or_above_facilities = Three_or_above_Facilities
        # Customization: Type the (1) searching distance and (2) three or above sports and outdoor facilities
        task3_three_or_above_facilities(2000, ['Badminton_court', 'swimming_pools', 'sports_grounds'])
        print("The Good and Bad coverage of three or above Sports Facilities is saved to the GDB, the file path is: " + os.path.join(temp_gdb))
        print("")

        print(
            "================-========== Task 3.5：Transportation Accessibility of All Sports and Outdoor Facilities ============================")
        arcpy.env.workspace = temp_gdb
        task_four_road_layer = base_path + "\\Raw_Data\\Road\\Road_network.shp"  # The transport network in Hong Kong
        task_four_facility_layer = base_path + "\\Raw_Data\\Facility data\\Badminton_court.shp"  # Customization: Change the shapefile of facilities
        search_distance = "100 Meters"  # Customization: The Searching distance
        analysis_result_layer = "task_four_analysisResult"
        task_four_final_result = traffic_access_analysis(task_four_road_layer, search_distance,
                                                         task_four_facility_layer, analysis_result_layer)
        print("Evaluating The Transport accessibility is completed, the result is saved to：" + os.path.join(temp_gdb,
                                                                                              analysis_result_layer))
        # Output the performance of the Transportation Accessibility of a certain type of sports facilities
        print(task_four_final_result + " of the facilities are within " + search_distance + " from the road network.")
        print("")
        print(
            "====================================================================================================================================")
        print("Congratulations!!!!! All Python Programming Tasks of LSGI3315 Group 6 are Error-free.")
        print(
            "This is the END of the LSGI3315 Group 6's Coding Section! Thank you very much for Running Our Group 6's Python Script! :)")


    except Exception as result:
        print(str(result))
