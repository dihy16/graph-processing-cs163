from RouteVarQuery import RouteVarQuery
from StopQuery import StopQuery
from PathQuery import PathQuery
from Graph import Graph

route_var_query = RouteVarQuery([])
route_var_query.inputFromJSON('data/vars.json')
stop_query = StopQuery([])
stop_query.inputFromJSON('data/stops.json')
path_query = PathQuery([])
path_query.inputFromJSON('data/paths.json')
graph = Graph()
graph.buildGraph(route_var_query, stop_query, path_query)
graph.shortestPathAllPairs(stop_query.stop_list, 'data/allPairs.json')


