from RouteVarQuery import RouteVarQuery
from StopQuery import StopQuery
from PathQuery import PathQuery
from Graph import Graph
from ContractionHierarchies import ContractionHierarchies

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

# """
# Save edges to file
# """
# graph.output_edges_as_JSON('data/GraphEdges.json')

"""
Input edges from file
"""
graph.input_edges_from_JSON('data/GraphEdges.json')
# graph.export_path_2_stops(0, 1)
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
"""
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
    ans = graph.dijkstra_one_pair(source, target)
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
print('RESULT:')
print('Vertex count: ', graph.num_nodes)
print('Edge count: ', graph.num_edges)
print('Dijkstra time: ', dijk_time)
print('CH compute time: ', CHtime)
print('CH query time: ', bidijkTime)
cnt = 0
for i in range(0, len(dijk_dist)):
    if abs(dijk_dist[i][2] - bidijk_dist[i]) > PRECISION_TOLERANCE:
        cnt += 1
        print(dijk_dist[i][0], dijk_dist[i][1], dijk_dist[i][2], bidijk_dist[i])
print('{} / {}'.format(cnt, len(dijk_dist)))