﻿from RouteVarQuery import RouteVarQuery
from StopQuery import StopQuery
from PathQuery import PathQuery
from Graph import Graph
from ContractionHierarchies import ContractionHierarchies
from TransitNodeRouting import TransitNodeRouting

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

"""
Input edges from file
"""
graph.input_edges_from_JSON('data/GraphEdges.json')
# start, stop = random.sample(uniqueIds, 2)
# start = stop_indices_dict[start]
# stop = stop_indices_dict[stop]
# path, coors = graph.export_path_2_stops(start, stop, uniqueIds, stop_list, 'data/coordinates.geojson')
# print(path)
# print(coors)
# """
# Run dijkstra for all pairs, then export to file
# """
# # print('Running Dijkstra on all pairs...')
# # start = time.time()
# # graph.dijkstra_all_pairs()
# # print(time.time() - start)
# # graph.export_dijkstra_all_pairs(uniqueIds, 'data/allPairs.json')

# """
# Finding top k stops, then export to file
# """
# # print('Finding top stops...')
# # kTopStops = graph.find_k_top_stops(uniqueIds, stop_list, 30)
# # stop_query.outputAsJSON(kTopStops, 'data/kStops.json')


"""
Comparing run time between Dijkstra and Bidirectional Dijkstra on CH 
# """
start = 0
stop = graph.num_nodes - 1
num_pairs = 10000
pairs = generate_multiple_pairs(start, stop, num_pairs)

dijk_time = 0
dijk_dist = []

print('Querying with Dijkstra...')
start = time.time() 
for pair in pairs:
    source, target = pair
    ans, _, _ = graph.dijkstra_one_pair_with_trace(source, target)
    dijk_dist.append((source, target, ans))
dijk_time = time.time() - start
print(dijk_time)

CH = ContractionHierarchies(graph)
start = time.time()
print('Computing CH...')
CH.preprocess_graph()
CHtime = time.time() - start
bidijk_dist = []

start = time.time() 

print('Querying with CH...')
for pair in pairs:
    source, target = pair 
    bidijk_dist.append(graph.bidirectional_dijkstra(source, target))
bidijkTime = time.time() - start

print(bidijkTime, 'secs')

TNR = TransitNodeRouting(graph, CH.rank)

start = time.time()
TNR.compute_TNR(250)
TNR_preprocess_time = time.time() - start

start = time.time()
print('Querying with TNR...')
TNR_dist = []
TNR_cnt = 0
no_access = 0
local = 0
for pair in pairs:
    s, t = pair
    isTNR, dist = TNR.shortest_path(s, t)
    if isTNR == -1:
        no_access += 1
    elif isTNR == 0:
        local += 1
    else:
        TNR_cnt += 1
    TNR_dist.append(dist)
    
TNR_time = time.time() - start

print('RESULT:')
print('Vertex count: ', graph.num_nodes)
print('Edge count: ', graph.num_edges)
print('Dijkstra time: ', dijk_time)
print('CH compute time: ', CHtime)
print('CH query time: ', bidijkTime)
print('TNR preprocess time: ', TNR_preprocess_time)
print('TNR time: ', TNR_time)
print('Num of TNR queries: ', no_access, local, TNR_cnt)
cnt = 0
for i in range(0, len(dijk_dist)):
    if abs(dijk_dist[i][2] - bidijk_dist[i]) > PRECISION_TOLERANCE:
        cnt += 1
        print(dijk_dist[i][0], dijk_dist[i][1], dijk_dist[i][2], bidijk_dist[i])
print('{} / {}'.format(cnt, len(dijk_dist)))
cnt = 0
for i in range(0, len(dijk_dist)):
    if abs(dijk_dist[i][2] - TNR_dist[i]) > PRECISION_TOLERANCE:
        cnt += 1
        print(dijk_dist[i][0], dijk_dist[i][1], dijk_dist[i][2], TNR_dist[i])
print('{} / {}'.format(cnt, len(dijk_dist)))

# print(len(graph.shortcuts))