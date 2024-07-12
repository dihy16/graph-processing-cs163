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
        self.Count = [0] * self.NumNodes

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
            rtree = Rtree.build_rtree(path_in_route.getLatList(), path_in_route.getLngList())
            closest_points, distances = Rtree.calc_distances(path_in_route, stops_coordinates[1:], rtree)
            for i in range(len(stops_in_route[1:])):
                startNode = stop_indices_dict[stops_in_route[i - 1].getStopId()] # the edge will start from this stop
                endNode = stop_indices_dict[stops_in_route[i].getStopId()]
                dist = distances[i]
                time_travelled = dist / speed
                self.Edges.append({
                    "startNode": startNode,
                    "endNode": endNode,
                    "time_travelled": time_travelled,
                    "dist": dist,
                    "closest_points": closest_points[i]
                })
                numEdge += 1
                print(numEdge, dist)
                
        endTime = time.time()
        print(f"{endTime - startTime} seconds")
                
    def buildGraph(self, route_var_query, stop_query, path_query):
        self.buildEdges(route_var_query, stop_query, path_query)
        
        # adjacency list has form : {node_0: edges idx from node_0, node_1: edges idx from node_1,...}
        for edge_idx in range(len(self.Edges)):
            self.AdjList[self.Edges[edge_idx]['startNode']].append(edge_idx)
  
    def Dijkstra(self, startNode):
        timeTaken = [float('inf')] * self.NumNodes
        timeTaken[startNode] = 0
        pq = []
        heapq.heappush(pq, (0, startNode))
        visited = [False] * self.NumNodes
        while pq:
            curNode_time, curNode = heapq.heappop(pq)
            
            if visited[curNode] is True or curNode_time > timeTaken[curNode]:
                continue
            
            visited[curNode] = True
            
            for edge_idx in self.AdjList[curNode]:
                
                edge = self.Edges[edge_idx]
                if visited[edge['endNode']] is True:
                    continue
                if edge['endNode'] not in timeTaken:
                    timeTaken[edge['endNode']] = float('inf')
                newTime = curNode_time + edge['time_travelled']
                if newTime < timeTaken[edge['endNode']]:
                    timeTaken[edge['endNode']] = newTime
                    heapq.heappush(pq, (newTime, edge['endNode']))
        return timeTaken
    
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
        
    def topStops(self):
        pass