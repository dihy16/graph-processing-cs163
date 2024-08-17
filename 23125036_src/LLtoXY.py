from pyproj import CRS, Transformer
import math
import geojson

crs_wgs84 = CRS.from_epsg(4326) 
crs_3405 = CRS.from_epsg(3405)  

transformer = Transformer.from_crs(crs_wgs84, crs_3405, always_xy=True)

def convertLngLatToXY(Lng, Lat):
    x, y = transformer.transform(Lng, Lat)
    return x, y

def getDistance(x1, y1, x2, y2):
    return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))

def export_line_string_to_GeoJSON(coordinates_list, stops_list, filename, color_list, width_list):
    features = []
    
    for i in range(len(coordinates_list)):
        line_feature = geojson.Feature(
            geometry=geojson.LineString(coordinates_list[i]), 
            properties={"stroke": color_list[i], "stroke-width": width_list[i]}
        )
        features.append(line_feature)
    
    for stops in stops_list:
        for s in stops:
            point_feature = geojson.Feature(geometry=geojson.Point(s))
            features.append(point_feature)
        
    feature_collection = geojson.FeatureCollection(features)
    
    with open(filename, 'w') as f:
        geojson.dump(feature_collection, f)
