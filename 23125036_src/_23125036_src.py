from RouteVarQuery import RouteVarQuery
from StopQuery import StopQuery
from PathQuery import PathQuery
from Graph import Graph
from ContractionHierarchies import ContractionHierarchies
from TransitNodeRouting import TransitNodeRouting
from LLtoXY import export_line_string_to_GeoJSON

import time
import random

def generate_multiple_pairs(start, stop, num_pairs):
    pairs = []
    for _ in range(num_pairs):
        pairs.append(tuple(random.sample(range(start, stop), 2)))
    return pairs
def compareDijkstraAndCH():
    pass

PRECISION_TOLERANCE = 1e-9

route_var_query = RouteVarQuery([])
route_var_query.inputFromJSON('data/vars.json')
stop_query = StopQuery([])
stop_query.inputFromJSON('data/stops.json')
path_query = PathQuery([])
path_query.inputFromJSON('data/paths.json')

stop_list = stop_query.getStopList()
uniqueIds = stop_query.buildUniqueIdStops(stop_list)
stop_indices_dict = stop_query.buildStopIdDict(stop_list)

num_nodes = len(stop_indices_dict)

graph = Graph(num_nodes)

"""
Build edges from scratch
"""
# start = time.time()
# graph.build_graph(route_var_query, stop_query, path_query, stop_indices_dict)
# print(time.time() - start)

# """0.
# Save edges to file
# """
# graph.output_edges_as_JSON('data/GraphEdges.json')
# print('Wrote edges to data/GraphEdges.json successfully.')

"""
Input edges from file
"""
graph.input_edges_from_JSON('data/GraphEdges.json')

"""
Compare paths of Dijkstra's and Bidirectional Dijkstra's on GeoJSON
"""
start, stop = random.sample(uniqueIds, 2)
start = stop_indices_dict[start]
stop = stop_indices_dict[stop]
coor1, stops1 = graph.export_path_2_stops(start, stop, uniqueIds, stop_list)
coor2, stops2 = graph.export_path_bidirect(start, stop, uniqueIds, stop_list)
coor_list = [coor1, coor2]
stops_list = [stops1, stops2]
color_list = ["#FF0000", "#0000FF"]
width_list = [10, 2]
export_line_string_to_GeoJSON(coor_list, stops_list, 'data/coordinates.geojson', color_list, width_list)
"""
Run dijkstra for all pairs, then export to file
"""
# print('Running Dijkstra on all pairs...')
# start = time.time()
# graph.dijkstra_all_pairs()
# print(time.time() - start)
# graph.export_dijkstra_all_pairs(uniqueIds, 'data/allPairs.json')

"""
Finding top k stops, then export to file
"""
# print('Finding top stops...')
# kTopStops = graph.find_k_top_stops(uniqueIds, stop_list, 30)
# stop_query.outputAsJSON(kTopStops, 'data/kStops.json')


"""
Comparing run time between Dijkstra and Bidirectional Dijkstra on CH 
# # """
start = 0
stop = graph.num_nodes - 1
num_pairs = 10000
pairs = generate_multiple_pairs(start, stop, num_pairs)

dijk_time = 0
dijk_dist = []
dijk_path = []
dijk_coor= []
print('Querying with Dijkstra...')
start = time.time() 
for pair in pairs:
    source, target = pair
    ans, path, coor = graph.dijkstra_one_pair_with_trace(source, target, uniqueIds)
    dijk_dist.append((source, target, ans))
    dijk_path.append(path)
    dijk_coor.append(coor)
dijk_time = time.time() - start

CH = ContractionHierarchies(graph)
start = time.time()
print('Preprocessing CH...')
CH.preprocess_graph()
CHtime = time.time() - start

bidijk_dist = []
bidijk_path = []
bidijk_coor = []

start = time.time() 
print('Querying with CH...')
for pair in pairs:
    source, target = pair 
    ans, path, coor = graph.bidirectional_dijkstra(source, target, uniqueIds)
    bidijk_dist.append(ans)
    bidijk_path.append(path)
    bidijk_coor.append(coor)
bidijkTime = time.time() - start


TNR = TransitNodeRouting(graph, CH.rank)
start = time.time()
print('Preprocessing TNR...')
TNR.compute_TNR(250, uniqueIds)
TNR_preprocess_time = time.time() - start

start = time.time()
print('Querying with TNR...')
TNR_dist = []
TNR_coors = []
TNR_cnt = 0
no_access = 0
local = 0
for pair in pairs:
    s, t = pair
    isTNR, dist, path, coors = TNR.shortest_path(s, t, uniqueIds)
    if isTNR == -1:
        no_access += 1
    elif isTNR == 0:
        local += 1
    else:
        TNR_cnt += 1
    TNR_dist.append(dist)
    TNR_coors.append(coors)
TNR_time = time.time() - start

print('=' * 50)
print('RESULT:')
print('Vertex count: ', graph.num_nodes)
print('Edge count: ', graph.num_edges)
print('=' * 50)
print('Total Dijkstras time: ', dijk_time)
print('Average Dijkstra query time: ', dijk_time / num_pairs)
print('=' * 50)
print('CH preprocessing time: ', CHtime)
print('Total CH query time: ', bidijkTime)
print('Average CH query time: ', bidijkTime / num_pairs)


# COMPARING RESULTS TO VERIFY CORRECTNESS OF CONTRACTION AND TNR
CH_error_dist = 0
for i in range(0, len(dijk_dist)):
    #print(dijk_dist[i][2])
    if abs(dijk_dist[i][2] - bidijk_dist[i]) > PRECISION_TOLERANCE:
        CH_error_dist += 1
        #print(dijk_dist[i][0], dijk_dist[i][1], dijk_dist[i][2], bidijk_dist[i])
print('Queries with different distances: {} / {}'.format(CH_error_dist, len(dijk_dist)))

CH_error_coor = 0
for i in range(0, len(dijk_coor)):
    if dijk_coor[i] != bidijk_coor[i]:
        CH_error_coor += 1
        #print(dijk_dist[i][0], dijk_dist[i][1], dijk_coor[i], bidijk_coor[i])
print('Queries with differenct coordinates: {} / {}'.format(CH_error_coor, len(dijk_coor)))
print('=' * 50)
print('TNR preprocess time: ', TNR_preprocess_time)
print('TNR time: ', TNR_time)
print('Average TNR query time: ', TNR_time / num_pairs)
print('Num of local queries: ', no_access + local)
print('Num of TNR queries: ', TNR_cnt)

TNR_error_dist = 0
for i in range(0, len(dijk_dist)):
    if abs(dijk_dist[i][2] - TNR_dist[i]) > PRECISION_TOLERANCE:
        TNR_error_dist += 1
        # print(dijk_dist[i][0], dijk_dist[i][1], dijk_dist[i][2], TNR_dist[i])
print('Queries with differenct distances: {} / {}'.format(TNR_error_dist, len(dijk_dist)))

TNR_error_coor = 0
for i in range(0, len(dijk_coor)):
    if dijk_coor[i] != TNR_coors[i]:
        TNR_error_coor += 1
        #print(dijk_dist[i][0], dijk_dist[i][1], dijk_coor[i], bidijk_coor[i])
print('Queries with differenct coordinates: {} / {}'.format(TNR_error_coor, len(dijk_coor)))

