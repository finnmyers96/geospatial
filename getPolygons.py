
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
from shapely.geometry import Polygon
from pyproj import Transformer
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

def transform_coordinates(easting, northing, from_epsg, to_epsg):
    """
    Transforms easting-northing coordinates to lon/lat
    
    Params:
        easting (float, req): easting location
        northing (float, req): northing location
        from_epsg (int, req): EPSG code for spatial projection easting and 
                              northing points are in
        to_epsg (int, req): EPSG code to convert to for lat/lon
        
    Returns:
        lon, lat (float): longitude and latitude of easting/northing coordinate
    """
    transformer = Transformer.from_crs(f'epsg:{from_epsg}', f'epsg:{to_epsg}', always_xy=True)
    lon, lat = transformer.transform(easting, northing)
    return lon, lat

def getPolygons(folderPath, from_epsg, to_epsg):
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
                    coords = geom.exterior.coords._coords[:, :2]
                    lonlat_coords = [transform_coordinates(x, y, from_epsg, to_epsg) for x, y in coords]
                    polygons[f'{f[:3]}'] = lonlat_coords
    return polygons
                    
polygon_dict = getPolygons(dir_path, 32145, 4326)

            
