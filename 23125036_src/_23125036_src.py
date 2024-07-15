from RouteVarQuery import RouteVarQuery
from StopQuery import StopQuery
from PathQuery import PathQuery
from Graph import Graph

import OutputData

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
#graph.buildGraph(route_var_query, stop_query, path_query, stop_indices_dict)
graph.inputGraphFromJSON('data/Edges.json')
#graph.DijkstraAllPairs(uniqueIds)
#graph.ExportShortestPathAllPairs(uniqueIds, 'data/allPairs.json')
#graph.outputEdgesAsJSON('data/Edges.json')
#OutputData.outputListDictsAsJSON('data/GraphEdges.json', graph.Edges)
kTopStops = graph.findKtopStops(uniqueIds, stop_list, 30)
stop_query.outputAsJSON(kTopStops, 'data/kStops.json')

