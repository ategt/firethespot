# coding: utf-8

from functools import reduce
import json
import shapefile
import sys

from math import sin, cos, sqrt, atan2, radians

# approximate radius of earth in km
R = 6373.0

def distance(p1, p2):
    """
        'p1' and 'p2' should both be dicts containing lat and lon keys, in degrees, and the result will be in kilometers.  The order of p1 and p2 does not affect the result.
    """
    lat1 = radians(p1['lat'])
    lon1 = radians(p1['lon'])
    lat2 = radians(p2['lat'])
    lon2 = radians(p2['lon'])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    
    return distance

def velocity(p1, p2):
    """
        'p1' and 'p2' must be dicts with a distance and speed keys.
    """

    return (p1['distance'] - p2['distance']) / (p1['time_frame'] - p2['time_frame'])

def speed(p1, p2):
    " Same as velocity, but always positive "
    return abs(velocity(p1, p2))

def load_all_shapes( path ):
    """ 
        Load shapes from shape file.

        'path' should be to the shape file without the extension, and all the shape files have to be in the same directory for the projram to load correctly.
    """
    reader = shapefile.Reader(path)
    shapes = reader.shapes()
    reader.dbf.close()
    reader.shx.close()
    reader.shp.close()

    return shapes

def extract_points( shapes ):
    """
        Convert a list within a list of shapes into points in [latitude, longitude] format.
    """
    all_points = [ shape.points for shape in shapes ]
    flattened_all_points = reduce(lambda acc, item: [*acc, *item], all_points, [])
    
    return flattened_all_points

def load_fire_coords( path ):
    """
        Returns a list of points from a path to a group of shape files.
            ( More information in load_all_shapes documentation. )
    """
    all_shapes = load_all_shapes(path)
    return extract_points( all_shapes )

def nearest_fires(here, dataset):
    """
        Takes a map {'lat':lat_value, 'lon': lon_value} to represent the location tested, and a list of latitude, longitude points and then returns a list of tuples containing lat/lon maps and distances, in kilometers, the tuples are sorted by distance, nearest first.
    """
    latlons = [{'lat':lat, 'lon': lon} for lon, lat in dataset ]
    distances = [(latlon, distance(latlon, here)) for latlon in latlons]
    sorted_fires = sorted(distances, key=lambda item: item[1])
    
    return sorted_fires

def add_time_frame(enhanced_dataset, time_frame):
    " Loops through all the maps in the dataset iterable, and adds a 'time_frame' field, containing the time_frame. "
    return [ {'latlon': latlon, 'distance': distance, 'time_frame': time_frame} for latlon, distance in enhanced_dataset]

def add_velocity(dataset1, dataset2):
    """
        Takes two iterables of dicts, adds a velocity key/value pair to the most recent.
        Overwrites any previous velocity key/value.

        'time_frame's are typically in hours into the past. Timeframe zero would be the most recent.
        Returns the most recent dataset, which should also be the dataset containing velocity information.

        Current version uses order to determine common fires.
        TODO: Use Latitude, Longitude to identify common fires in the datasets.
        TODO: Consider checking for out of sequence/phase items in the datasets.  (If in the first pair of common fire values, the first fire is the most recent, and then later on, in another common fire the second fire is more recent then a bug has likely been discovered.)
    """

    for fire1, fire2 in zip(dataset1, dataset2):
        velocity_value = velocity(fire1, fire2)

        if fire1['time_frame'] > fire2['time_frame']:
            fire2['velocity'] = velocity_value
        elif fire1['time_frame'] < fire2['time_frame']:
            fire2['velocity'] = velocity_value
        else:
            raise Exception("The same dataset was passed as both arguments.")

    return dataset2 if dataset1[0]['time_frame'] > dataset2[0]['time_frame'] else dataset1

def nearest_moving_fire(dataset, threashold = 0.01):
    " Takes a dataset with velocity and distance attributes and returns the nearest one. "
    sorted_dataset = sorted(dataset, key=lambda item: item['distance'])

    return [ fire for fire in sorted_dataset if fire['velocity'] > threashold][0]

def load_to_enhanced_plots( path, here, retrieval_time ):
    """
        Convert a path string into a list of dicts composed of 'latlon': dicts, 'distance', 'time_frame', sorted by distance from 'here' dict, nearest first.
    """
    dataset = load_fire_coords( path )
    enhanced_dataset = nearest_fires( here, dataset )
    enhanced_dataset = add_time_frame(enhanced_dataset, retrieval_time )
    
    return enhanced_dataset
