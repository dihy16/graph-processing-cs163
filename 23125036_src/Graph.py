from collections import defaultdict
from StopQuery import StopQuery
from PathQuery import PathQuery
from Path import Path
import Rtree

class Graph:
    def __init__(self):
        self.AdjMatrix = defaultdict(list)
        self.Edges = []
        
    def buildEdges(self, route_var_query, stop_query, path_query):
            
        "Initialize list of edges for the graph from 3 lists: routeVars, stops, and paths"
        
        #create dict that maps stops' IDs to indices
        
        stop_indices_dict = {}
        
        uniqueRouteId_stops = list({stop.getStopId() for stop in stop_query.stop_list})
        for i in range(len(uniqueRouteId_stops)):
            stop_indices_dict[uniqueRouteId_stops[i]] = i
        
        numEdge = 0
        
        for route_var in route_var_query.RouteVar_list:
            
            speed = route_var.getDistance() / (route_var.getRunningTime() * 60.00)
            
            # return list of stops in a particular routeVar
            stops_in_route = StopQuery(stop_query.searchByRouteId(str(route_var.getRouteId()))).searchByRouteVarId(str(route_var.getRouteVarId()))
            # return a path in a particular routeVar
            path_in_route = PathQuery(path_query.searchByRouteId(str(route_var.getRouteId()))).searchByRouteVarId(str(route_var.getRouteVarId()))[0]
            
            startEdge = stop_indices_dict[stops_in_route[0].getStopId()] # the edge will start from this stop
            
            stops_coordinates = [(stop.getLat(), stop.getLng()) for stop in stops_in_route]
            rtree = Rtree.build_rtree_index(path_in_route.getLatList(), path_in_route.getLngList())
            closest_points, distances = Rtree.find_closest_points_with_narrowing(path_in_route, stops_coordinates[1:], rtree)
            for i in range(len(stops_in_route[1:])):
                startEdge = stop_indices_dict[stops_in_route[i - 1].getStopId()] # the edge will start from this stop
                endEdge = stop_indices_dict[stops_in_route[i].getStopId()]
                dist = distances[i]
                self.Edges.append((startEdge, endEdge, dist / speed, dist, closest_points[i]))
                numEdge += 1
                print(numEdge)
                

    def buildGraph(self, route_var_query, stop_query, path_query):
        self.buildEdges(route_var_query, stop_query, path_query)
        for i in range(len(self.Edges)):
            self.AdjMatrix[self.Edges[i][0]].append(i)
            
    def Dijkstra(self):
        pass

