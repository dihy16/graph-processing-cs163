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

def graph_to_geojson(nodes, graph):
    features = []
    
    for node1, connected_nodes in graph.items():
        for node2 in connected_nodes:
            if node1 in nodes and node2 in nodes:
                # Get the coordinates of the two connected nodes
                point1 = nodes[node1]
                point2 = nodes[node2]
                
                # Create a LineString between these two points
                line = geojson.LineString([point1, point2])
                
                # Create a GeoJSON feature for this edge
                feature = geojson.Feature(
                    geometry=line,
                    properties={"from": node1, "to": node2}
                )
                
                features.append(feature)
    
    # Create a FeatureCollection from all the features
    feature_collection = geojson.FeatureCollection(features)
    return feature_collection

def drawWays(handler):
    features = []

    for way in handler.ways:
        coordinates = []
        for node_id in way:
            if node_id in handler.nodes:
                coordinates.append(handler.nodes[node_id][::-1])  # Reverse to get (lon, lat)
    
        if len(coordinates) > 1:  # Ensure it's a valid LineString with at least two points
            feature = geojson.Feature(geometry=geojson.LineString(coordinates))
            features.append(feature)

    # Create a GeoJSON FeatureCollection
    feature_collection = geojson.FeatureCollection(features)
    return feature_collection

def drawNodes(handler):
    features = []

    for node_id, node in handler.nodes.items():
        lat, lon = node  # Assuming node is a tuple (lat, lon)
        feature = geojson.Feature(
            geometry=geojson.Point((lon, lat)),  # Reverse to get (lon, lat)
            properties={"id": node_id}
        )
        features.append(feature)

    feature_collection = geojson.FeatureCollection(features)
    return feature_collection

def drawNodes(handler, node_list):
    features = []
    for node in node_list:
        lat, lon = handler.nodes[node]
        feature = geojson.Feature(
            geometry=geojson.Point((lon, lat)),  # Reverse to get (lon, lat)
            properties={"id": node}
        )
        features.append(feature)
    
    # Create a GeoJSON FeatureCollection
    feature_collection = geojson.FeatureCollection(features)
    return feature_collection

def drawEdgesOSM(handler, path_list):
    features = []
    
    for path in path_list:
        coordinates = []
        for node in path:
            coordinates.append(handler.nodes[node][::-1])
            
        if len(coordinates) > 1:
            feature = geojson.Feature(geometry=geojson.LineString(coordinates))
            features.append(feature) 
            
    feature_collection = geojson.FeatureCollection(features)
    return feature_collection