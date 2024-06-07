
"""
This script reads all shapefiles in a directory, and extracts the AOI polygons 
stored in the shapefile to a geopandas Polygon to query Planet Imagery downloads
through their API. The code logic assumes only one polygon is stored in each
shapefile.

Harrison Myers
6/7/2024

Dependencies: 
    -- os
    -- geopandas (pip install geopandas)
    -- shapely (pip install shapely)
"""
import geopandas as gpd
from shapely.geomety import Polygon
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

def getPolygons(folderPath, sitenames):
    """
    Reads all shapefiles in a directory and stores their respective polygons
    in a dictionary
    Params:
        -- folderPath (str, req): Path to folder where shapefiles are stored
    returns:
        -- polygons (dict): Dictionary of polygons indexed by first two letters
                            of site name
    """
    polygons = {}
    for f in os.listdir(folderPath):
        if f.endswith('.shp'): # only read shapefiles
            fpath = os.path.join(folderPath, f) # get path to shapefile
            gdf = gpd.read_file(fpath) # read shapefile
            for geom in gdf.geometry:
                if isinstance(geom, Polygon):
                    polygons[f'{f[:3]}'] = geom
    return polygons
                    
                    
            
            
