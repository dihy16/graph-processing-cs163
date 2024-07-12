from collections import defaultdict
from StopQuery import StopQuery
from PathQuery import PathQuery
import Rtree
import time
import heapq
import json

class Graph:
    
    def __init__(self):
        self.AdjList = defaultdict(list)
        self.NumNodes = 0
        self.Edges = []
    
    def buildUniqueIdStops(self, stop_list):
        return list({stop.getStopId() for stop in stop_list})

    def buildStopIdDict(self, stop_list):
        stop_indices_dict = {}
        
        uniqueRouteId_stops = self.buildUniqueIdStops(stop_list)
        for i in range(len(uniqueRouteId_stops)):
            stop_indices_dict[uniqueRouteId_stops[i]] = i
        
        return stop_indices_dict

    def buildEdges(self, route_var_query, stop_query, path_query):
            
        "Initialize list of edges for the graph from 3 lists: routeVars, stops, and paths"
        
        #create dict that maps stops' IDs to indices
        startTime = time.time()
        self.NumNodes = len(self.buildUniqueIdStops(stop_query.stop_list))
        stop_indices_dict = self.buildStopIdDict(stop_query.stop_list)
        
        numEdge = 0
        
        for route_var in route_var_query.RouteVar_list:
            
            speed = route_var.getDistance() / (route_var.getRunningTime() * 60.00)
            
            # return list of stops in a particular routeVar
            stops_in_route = StopQuery(stop_query.searchByRouteId(str(route_var.getRouteId()))).searchByRouteVarId(str(route_var.getRouteVarId()))
            # return a path in a particular routeVar
            path_in_route = PathQuery(path_query.searchByRouteId(str(route_var.getRouteId()))).searchByRouteVarId(str(route_var.getRouteVarId()))[0]
            
            stops_coordinates = [(stop.getLat(), stop.getLng()) for stop in stops_in_route]
            rtree = Rtree.build_rtree_index(path_in_route.getLatList(), path_in_route.getLngList())
            closest_points, distances = Rtree.find_closest_points_with_narrowing(path_in_route, stops_coordinates[1:], rtree)
            for i in range(len(stops_in_route[1:])):
                startEdge = stop_indices_dict[stops_in_route[i - 1].getStopId()] # the edge will start from this stop
                endEdge = stop_indices_dict[stops_in_route[i].getStopId()]
                dist = distances[i]
                self.Edges.append((startEdge, endEdge, dist / speed, dist, closest_points[i]))
                numEdge += 1
                print(numEdge, dist)
                
        endTime = time.time()
        print(f"{endTime - startTime} seconds")
                
    def buildGraph(self, route_var_query, stop_query, path_query):
        self.buildEdges(route_var_query, stop_query, path_query)
        
        # adj list has form : {node0: edges, node1: edges,...}
        for i in range(len(self.Edges)):
            self.AdjList[self.Edges[i][0]].append(i)
            
    def Dijkstra(self, startNode):
        
        # distance array
        distances = [float('inf')] * self.NumNodes
        distances[startNode] = 0
        
        # priority queue
        pq = []
        
        heapq.heappush(pq, (0, startNode))
        predecessors = [None] * self.NumNodes
        visited = [False] * self.NumNodes

        while pq:
            u_dist, u = heapq.heappop(pq)
            
            for edge in self.AdjList[u]:
                if distances[self.Edges[edge][1]] > distances[u] + self.Edges[edge][2]:
                    distances[self.Edges[edge][1]] = distances[u] + self.Edges[edge][2]
                    heapq.heappush(pq, (distances[self.Edges[edge][1]], self.Edges[edge][1]))
            
        return distances
       
    def shortestPathAllPairs(self, stop_list, filename):
        with open(filename, 'w', encoding='utf8') as fout:
            uniqueStopIds = self.buildUniqueIdStops(stop_list)
            for u in range(self.NumNodes):
                result = self.Dijkstra(u)
                print('Calculated shortest path on {}/4396'.format(u))
                for v in range(self.NumNodes):
                    if u != v and v in result:
                        json.dump((uniqueStopIds[u], uniqueStopIds[v], result[v]), fout, ensure_ascii=False)
                        fout.write('\n')
    
    def shortestPath2Stops(self, start_stop_id, end_stop_id, stop_list):
        stop_indices_dict = self.buildStopIdDict(stop_list)
        shortestDist = self.Dijkstra(stop_indices_dict[start_stop_id])
        print(f"{start_stop_id},{end_stop_id} : {shortestDist[end_stop_id]}")