from rtree import index
import LLtoXY
import math

def build_rtree_index(lat_list, lng_list):
    rtree_idx = index.Index()
    for idx, (lat, lng) in enumerate(zip(lat_list,lng_list)):
        x, y = LLtoXY.convertLngLatToXY(lng, lat)
        rtree_idx.insert(idx, (x, y, x, y)) 
    return rtree_idx

def find_closest_points_with_narrowing(path, given_points, rtree_idx):
    closest_points = []
    distances = []
    current_index = 0 
    dist = 0
    for lat_given, lng_given in given_points:
        x_given, y_given = LLtoXY.convertLngLatToXY(lng_given, lat_given)
        nearest_index = list(rtree_idx.nearest((x_given, y_given), 1))[0]
        x_path, y_path = LLtoXY.convertLngLatToXY(path.getLngList()[current_index], path.getLatList()[current_index])
        dist = math.sqrt((x_given - x_path) ** 2 + (y_given - y_path) ** 2)
        closest_points.append([(path.getLatList()[current_index], path.getLngList()[current_index])])
        for idx in range(current_index + 1, nearest_index + 1):
            closest_points.append([(path.getLngList()[idx], path.getLatList()[idx])])
            x1, y1 = LLtoXY.convertLngLatToXY(path.getLngList()[idx - 1], path.getLatList()[idx - 1])
            x2, y2 = LLtoXY.convertLngLatToXY(path.getLngList()[idx], path.getLatList()[idx])
            dist += math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        distances.append(dist)
        current_index = nearest_index + 1
        # narrow down the search space for the next point
        # rtree_idx = build_rtree_index(path.getLatList()[current_index:], path.getLngList()[current_index:])
        
    return closest_points, distances
