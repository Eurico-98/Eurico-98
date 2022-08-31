import argparse
import pandas as pd
import geopandas as gpd
import shapely.geometry 
import shapely.ops
from pyproj import Transformer

def get_ref_point_from_nearest_point(lat, lon, csvFile):

    # get coords of points from data frame
    df = pd.read_csv(csvFile)

    # create new dataframe with a column for points
    coords_has_df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.export_res_1, df.export_res_2))
    
    # get list of points from dataframe
    coords = shapely.geometry.MultiPoint(gpd.points_from_xy(df.export_res_1, df.export_res_2))
    
    # remove master point
    coords = coords.geoms[1:]
    
    # convert coords to point
    origin_point = shapely.geometry.Point(float(lon), float(lat))
    
    # get the nearest point to point received in parameters
    ref_point = shapely.ops.nearest_points(origin_point, coords)[1]
    
    # iterate df_coords_has_df to find nearest point and subtract its values to the rest of the values int the original df
    for line in coords_has_df.index:
        if (coords_has_df.iloc[line, -1] == ref_point):
            break
      
    df_points = df.iloc[1:, 3:]
    
    col_index = 3
    for x in df_points.columns:
        if(x != "geometry"):
            df_points[x] = df_points[x] - coords_has_df.iloc[line, col_index]
            col_index += 1
    
    df.iloc[1:, 3:] = df_points
    
    # remove geometry column that has inserted in line 15
    df = df.drop('geometry', axis=1)
    
    # create new file
    newFinalCsv = create_final_corrected_csv(csvFile)
    
    # write changes to new file
    df.to_csv(newFinalCsv,index=False)


def get_ref_point_from_rectangle(lat, lon, lat2, lon2, csvFile):
    
    # convert lat and long from WSg84 (epsg:4326) to metric epsg:3857
    transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
    x,  y  = transformer.transform(lon,  lat )
    x2, y2 = transformer.transform(lon2, lat2)
        
    # get 4 corners of the rectangle has shapely points
    corner1 = shapely.geometry.Point(float(x), float(y))
    corner2 = shapely.geometry.Point(float(x2), float(y2))
    corner3 = shapely.geometry.Point(float(x), float(y2))
    corner4 = shapely.geometry.Point(float(x2), float(y))
    
    rectangle = shapely.geometry.Polygon([[p.x, p.y] for p in [corner1, corner2, corner3, corner4]])
        
    # convert buffer to geoDataframe to convert coordinate system
    gdf = gpd.GeoDataFrame(index=[0], crs='EPSG:3857', geometry=[rectangle])
    converted_buffer = gdf.to_crs(4326)
    
    df = pd.read_csv(csvFile)

    # Dataframe to GeoSeries
    s = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.export_res_1, df.export_res_2))
    s.crs = "EPSG:4326" # set coordinate system
    
    # gets all the points inside the polygon passed returns a vector data of POINT geometry
    points_inside_poly = gpd.clip(s, converted_buffer, keep_geom_type=False)
      
    if(len(points_inside_poly) > 0):
        
        # create list with averages of mesurments
        average_point = []

        # iterate columns to calculate average of the mesurments of the points
        for column in range(len(points_inside_poly.columns)-1):
            if column > 2:
                average_point.append(points_inside_poly.iloc[:, column].mean())
                       
        # Subtraction of lines -> subtrackt offset of the points to the reference point
        i = 0
        sub = pd.DataFrame()
        for column in range(len(df.columns)-1):
            if column > 2:
                col_name = df.columns[column]
                sub[col_name] = df.iloc[:, column] - average_point[i]
                i += 1

        # Concatenate all columns into one dataframe
        final = pd.concat([df.iloc[:, 0:3],sub.iloc[:,0:]],axis=1)

        # create new file
        newFinalCsv = create_final_corrected_csv(csvFile)
        
        # write changes to new file
        final.to_csv(newFinalCsv,index=False)
    

def get_ref_point_from_circle(lat, lon, radius, csvFile):
    
    # convert lat and long from WSg84 (epsg:4326) to metric epsg:3857
    transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
    x, y = transformer.transform(lon, lat)
    
    # get all points inside circle with center and radius
    center = shapely.geometry.Point(float(x), float(y))
    buffer = center.buffer(radius)
    
    # convert buffer to geoDataframe to convert coordinate system
    gdf = gpd.GeoDataFrame(index=[0], crs='EPSG:3857', geometry=[buffer])
    converted_buffer = gdf.to_crs(4326)
    
    df = pd.read_csv(csvFile)

    # Dataframe to GeoSeries
    s = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.export_res_1, df.export_res_2))
    s.crs = "EPSG:4326" # set coordinate system
    
    # gets all the points inside the polygon passed returns a vector data of POINT geometry
    points_inside_poly = gpd.clip(s, converted_buffer, keep_geom_type=False)
   
    if(len(points_inside_poly) > 0):
        
        # create list with averages of mesurments
        average_point = []

        # iterate columns to calculate average of the mesurments of the points
        for column in range(len(points_inside_poly.columns)-1):
            if column > 2:
                average_point.append(points_inside_poly.iloc[:, column].mean())
                       
        # Subtraction of lines -> subtrackt offset of the points to the reference point
        i = 0
        sub = pd.DataFrame()
        for column in range(len(df.columns)-1):
            if column > 2:
                col_name = df.columns[column]
                sub[col_name] = df.iloc[:, column] - average_point[i]
                i += 1

        # Concatenate all columns into one dataframe
        final = pd.concat([df.iloc[:, 0:3],sub.iloc[:, 0:]],axis=1)

        # create new file
        newFinalCsv = create_final_corrected_csv(csvFile)
        
        # write changes to new file
        final.to_csv(newFinalCsv,index=False)


def get_ref_point_from_std(csvFile):
    
    df = pd.read_csv(csvFile)
    
    min_std = 0
    line_index = 0
    aux = 0
    
    for i in df.index:
        
        # initialize min_std
        if(i == 1):
            min_std = df.iloc[i, 3:].std()
            line_index = i
        
        elif(i > 1):
            aux = df.iloc[i, 3:].std()
            if(aux < min_std):
                min_std = aux
                line_index = i
        
    # in case input file only has header and master line there will be no other values to subtract
    if(line_index > 0):         
        
        # first correct average velocity column
        df.iloc[1:,2] = df.iloc[1:,2] - df.iloc[line_index,2]
        
        # get first line from original csv file
        first_line = df.iloc[0, :]
        
        # put coordinates of reference point in first line
        first_line.iloc[0:2] = df.iloc[line_index, 0:2]
        
        # put first line in final corrected csv file
        df.iloc[0, :] = first_line
         
        df_points = df.iloc[1:, 3:]
        
        # ajust index of line with the reference point -> remove one representing the first line
        line_index -= 1
        
        for col_index in range(len(df_points.columns)):
            df_points.iloc[:, col_index] = df_points.iloc[:, col_index] - df_points.iloc[line_index, col_index]
        
        df.iloc[1:, 3:] = df_points
        
    # create new file
    newFinalCsv = create_final_corrected_csv(csvFile)
    
    # write changes to new file
    df.to_csv(newFinalCsv,index=False,na_rep="NaN")
    

def get_ref_point_from_median(csvFile):
    
    df = pd.read_csv(csvFile)
    df_points = df.iloc[1:, 3:]
    
    for x in df_points.columns:
        df_points[x] = df_points[x] - df_points[x].mean()
    
    df.iloc[1:, 3:] = df_points
    
    # create new file
    newFinalCsv = create_final_corrected_csv(csvFile)
    
    # write changes to new file
    df.to_csv(newFinalCsv,index=False)


def get_ref_point_from_avg_velo(csvFile):
    
    df = pd.read_csv(csvFile)
    df_points = df.iloc[1:, 3:]
    
    min_avg_velo = df.iloc[1:, 3].min()
    
    for x in df_points.columns:
        df_points[x] = df_points[x] - min_avg_velo
    
    df.iloc[1:, 3:] = df_points
    
    # create new file
    newFinalCsv = create_final_corrected_csv(csvFile)
    
    # write changes to new file
    df.to_csv(newFinalCsv,index=False)


def create_final_corrected_csv(csvFile):
    
    path = csvFile.split("/")
    newFinalCsv = ''
    
    for file in path:
        if(len(file.split(".")) == 2 and file.split(".")[1] == "csv"):
            newFinalCsv += file.split(".")[0] + "_corrected.csv"
    
    f = open(newFinalCsv, 'w')
    f.close()
    
    return newFinalCsv


if __name__ == "__main__":
    
    # set parser
    parser = argparse.ArgumentParser(description='''
    Option 1:
        Get ref point nearest to fixed point - example input:
        get_reference_point -op 1 -lat 45 -lon 56 -csvFile (...)/final.csv
        
        Outputs a file named final_corrected.csv in the same location of the script
    ----------------------------------------------------------------------------------------------------
    Option 2:
        Get ref point from rectangular area using two points - example input:
        get_reference_point -op 2 -lat 45 -lon 56 -lat2 69 -lon2 420 -csvFile (...)/final.csv
        
        Outputs a file named final_corrected.csv in the same location of the script
    ----------------------------------------------------------------------------------------------------
    Option 3:
        Get ref point from circular area using fixed point and radius - example input:
        get_reference_point -op 3 -lat 45 -lon 56 -dist 100 -csvFile (...)/final.csv
        
        Outputs a file named final_corrected.csv in the same location of the script
    ----------------------------------------------------------------------------------------------------
    Option 4:
        Automatically select ref point from points with lowest standard deviation - example input:
        get_reference_point -op 4 -csvFile (...)/final.csv
        
        Outputs a file named final_corrected.csv in the same location of the script
    ----------------------------------------------------------------------------------------------------
    Option 5:
        Get ref point based on median of all points - example input:
        get_reference_point -op 5 -csvFile (...)/final.csv
        
        Outputs a file named final_corrected.csv in the same location of the script
    ----------------------------------------------------------------------------------------------------
    Option 6:
        Get ref point based on lowest average velocity - example input:
        get_reference_point -op 6 -csvFile (...)/final.csv
        
        Outputs a file named final_corrected.csv in the same location of the script
    ----------------------------------------------------------------------------------------------------
    ''', formatter_class=argparse.RawTextHelpFormatter)
    
    # used for options 1 2 and 3
    parser.add_argument('-lat', '--lat', metavar='', required=False, help='insert valid latitude')
    parser.add_argument('-lon', '--lon', metavar='', required=False, help='insert valid longitude')
    
    # just for option 2
    parser.add_argument('-lat2', '--lat2', metavar='', required=False, help='insert valid second latitude')
    parser.add_argument('-lon2', '--lon2', metavar='', required=False, help='insert valid second longitude')
    
    # just for option 3
    parser.add_argument('-radius', '--radius', metavar='', required=False, help='insert valid radius distance')
    
    # for all options
    parser.add_argument('-op', '--op', metavar='', required=True, help='insert one option from: 1, 2, 3, 4, 5')
    parser.add_argument('-csvFile', '--csvFile', metavar='', required=False, help='insert valid path to final.csv file')
    args = parser.parse_args()
    
    if(int(args.op) == 1):
        
        if(args.csvFile is None): 
            print("Please insert a valid path for csv file")
        else:
            get_ref_point_from_nearest_point(args.lat, args.lon, args.csvFile)
        
    elif(int(args.op) == 2):
        
        if(args.csvFile is None): 
            print("Please insert a valid path for csv file")
        else:
            if(args.lat is None or args.lon is None or args.lat2 is None or args.lon2 is None): 
                print("Please insert valid latitude and longitude values")
            else:
                get_ref_point_from_rectangle(args.lat, args.lon, args.lat2, args.lon2, args.csvFile)
        
    elif(int(args.op) == 3):
        
        if(args.csvFile is None): 
            print("Please insert a valid path for csv file")
        else:
            if(args.lat is None or args.lon is None or args.radius is None): 
                print("Please insert valid values for latitude, longitude and radius")
            else:
                get_ref_point_from_circle(args.lat, args.lon, int(args.radius), args.csvFile)
        
    elif(int(args.op) == 4):
        
        if(args.csvFile is None): 
            print("Please insert a valid path for csv file")
        else:
            get_ref_point_from_std(args.csvFile)
        
    elif(int(args.op) == 5):
        if(args.csvFile is None): 
            print("Please insert a valid path for csv file")
        else:
            get_ref_point_from_median(args.csvFile)
            
    elif(int(args.op) == 6):
        if(args.csvFile is None): 
            print("Please insert a valid path for csv file")
        else:
            get_ref_point_from_avg_velo(args.csvFile)