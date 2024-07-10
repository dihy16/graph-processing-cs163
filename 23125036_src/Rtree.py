from rtree import index
import LLtoXY
import math

def build_rtree_index(lat_list, lng_list):
    rtree_idx = index.Index()
    for idx, (lat, lng) in enumerate(zip(lat_list,lng_list)):
        y, x = LLtoXY.convertLngLatToXY(lng, lat)
        rtree_idx.insert(idx, (x, y, x, y)) 
    return rtree_idx

def find_closest_points_with_narrowing(path, given_points, rtree_idx):
    closest_points = []
    distances = []
    current_index = 0  # start searching from the beginning of the path
    
    for x_given, y_given in given_points:
        
        nearest_index = list(rtree_idx.nearest((x_given, y_given), 1))[0]
        closest_point = (path.getLatList()[nearest_index], path.getLngList()[nearest_index])
        x, y = closest_point
        dist = math.sqrt((x_given - x) ** 2 + (y_given - y) ** 2)
        distances.append(dist)
        
        closest_points.append([(path.getLatList()[idx], path.getLngList()[idx]) for idx in range(current_index, nearest_index + 1)])
            
        current_index = max(current_index, nearest_index)
        # narrow down the search space for the next point
        # rtree_idx = build_rtree_index(path.getLatList()[current_index:], path.getLngList()[current_index:])
        
    return closest_points, distances
