from RouteVarQuery import RouteVarQuery
from StopQuery import StopQuery
from PathQuery import PathQuery
from Graph import Graph

import time

route_var_query = RouteVarQuery([])
route_var_query.inputFromJSON('data/vars.json')
stop_query = StopQuery([])
stop_query.inputFromJSON('data/stops.json')
path_query = PathQuery([])
path_query.inputFromJSON('data/paths.json')

stop_list = stop_query.getStopList()
uniqueIds = stop_query.buildUniqueIdStops(stop_list)
stop_indices_dict = stop_query.buildStopIdDict(stop_list)

NumNodes = len(stop_indices_dict)

graph = Graph(NumNodes)

# build edges from scratch
#graph.buildGraph(route_var_query, stop_query, path_query, stop_indices_dict)

# input edges from file
graph.inputGraphFromJSON('data/Edges.json')

# run dijkstra for all pairs, then export to file
#graph.DijkstraAllPairs()
#graph.ExportShortestPathAllPairs(uniqueIds, 'data/allPairs.json')

#save edges to file
#OutputData.outputListDictsAsJSON('data/GraphEdges.json', graph.Edges)

# finding top k stops, then export to file
#kTopStops = graph.findKtopStops(uniqueIds, stop_list, 30)
#stop_query.outputAsJSON(kTopStops, 'data/kStops.json')

# comparing results between Dijkstra's and Bidirectional Dijkstra's
# for source in range(2, 3):
#     true = graph.Dijkstra(source)
#     for target in range(graph.NumNodes):
#         if source == target or target not in true:
#             continue
#         print(uniqueIds[source], uniqueIds[target])
#         shortest_path = graph.Bidirectional_Dijkstra(source, target)
#         if shortest_path != true[target]:
#             print('{} , {} : true: {} - vjp{}'.format(uniqueIds[source], uniqueIds[target], true[target], shortest_path))
            
# comparing run time between normal Dijkstra and Bidirectional Dijkstra
dijk_time = 0
bidijk_time = 0

dijk_dist = []
bidijk_dist = []

start = time.time() 
for source in range(0, 10):
     for target in range(0, 1000):
        print('dijk {} {}'.format(source, target))
        dijk_dist.append(graph.Dijkstra_1_Pair(source, target))
dijk_time = time.time() - start

start = time.time() 
for source in range(0, 10):
     for target in range(0, 1000):        
        print('BIdijk {} {}'.format(source, target))
        bidijk_dist.append(graph.Bidirectional_Dijkstra(source, target))
bidijk_time = time.time() - start

print(dijk_time, bidijk_time)
        
for i in range(0, 1000):
    if dijk_dist[i] != bidijk_dist[i]:
        print(dijk_dist[i], bidijk_dist[i])