from collections import defaultdict 
from StopQuery import StopQuery

class Graph:
    def __init__(self):
        self.AdjList = defaultdict(list)
        self.Edges = []
        
    def buildEdges(self, route_var_query, stop_query):
        
        "Initialize list of edges for the graph from 3 lists: routeVars, stops, and paths"
        
        #create dict that maps stops' IDs to indices
        stop_indices_dict = {}
        uniqueRouteId_stops = list({stop.getRouteId() for stop in stop_query.stop_list})
        for i in range(len(uniqueRouteId_stops)):
            stop_indices_dict[uniqueRouteId_stops[i].getStopId()] = i
        
        for route_var in route_var_query.RouteVar_list:
            
            # return list of stops in a particular routeVar
            stops_in_route = StopQuery(stop_query.searchByRouteId(str(route_var.getRouteId()))).searchByRouteVarId(str(route_var.getRouteVarId()))
            startEdge = stop_indices_dict[stops_in_route[0].getStopId()] # the edge will start from this stop
            for stop in stops_in_route[1:]:
                endEdge = stop_indices_dict[stop.getStopId()] # the edge will end at this stop
                self.Edges.append((startEdge, endEdge))
                startEdge = endEdge

    def buildGraph(self):
        for i in range(len(self.Edges)):
            self.AdjList[self.Edges[i][0]].append(i)

