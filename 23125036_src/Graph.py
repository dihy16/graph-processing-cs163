from collections import defaultdict
from StopQuery import StopQuery
from PathQuery import PathQuery
import time
import heapq
import json
import LLtoXY
import math

class Graph:
    def __init__(self, NumNodes):
        self.AdjList = defaultdict(list)
        self.NumNodes = NumNodes
        self.Edges = []

    def buildEdges(self, route_var_query, stop_query, path_query, stop_indices_dict):
            
        "Initialize list of edges for the graph from 3 lists: routeVars, stops, and paths"
        
        #create dict that maps stops' IDs to indices
        startTime = time.time()
        
        numEdge = 0
        
        for route_var in route_var_query.RouteVar_list:
            
            speed = route_var.getDistance() / (route_var.getRunningTime() * 60.00)
            route_id = str(route_var.getRouteId())
            route_var_id = str(route_var.getRouteVarId())
            
            # return list of stops in a particular routeVar
            stops_in_route = StopQuery(stop_query.searchByRouteId(route_id))
            stops_in_route_var = stops_in_route.searchByRouteVarId(route_var_id)
            
            # return a path in a particular routeVar
            path_in_route = PathQuery(path_query.searchByRouteId(route_id))
            path_in_rv = path_in_route.searchByRouteVarId(route_var_id)[0]
            pathLngList = path_in_rv.getLngList()
            pathLatList = path_in_rv.getLatList()
            
            minDistIdx= 0
            startNode = stop_indices_dict[stops_in_route_var[0].getStopId()] # the edge will start from this stop
            for i in range(1, len(stops_in_route_var)):
                curStop = stops_in_route_var[i]
                endNode = stop_indices_dict[curStop.getStopId()]
                y_stop, x_stop = LLtoXY.convertLngLatToXY(curStop.getLng(), curStop.getLat())    
                min_dist = float('inf')
                for j1 in range(minDistIdx, len(pathLngList)):
                    y1, x1 = LLtoXY.convertLngLatToXY(path_in_rv.getLngList()[j1], path_in_rv.getLatList()[j1])
                    curDist = math.sqrt((x1 - x_stop) ** 2 + (y1 - y_stop) ** 2)
                    if curDist < min_dist:
                        min_dist = curDist
                        ind = j1
                        
                ListCoor = []
                ListCoor.append((pathLatList[minDistIdx], pathLngList[minDistIdx]))
                
                dist = 0
                for idx in range(minDistIdx, ind):
                    y1, x1 = LLtoXY.convertLngLatToXY(pathLngList[idx], pathLatList[idx])
                    y2, x2 = LLtoXY.convertLngLatToXY(pathLngList[idx + 1], pathLatList[idx + 1])
                    dist += LLtoXY.getDistance(x1, y1, x2, y2)
                    ListCoor.append((pathLatList[idx + 1], pathLngList[idx + 1]))
                
                minDistIdx = ind
                    
                time_travelled = dist / speed
                self.Edges.append({
                    'startNode': startNode,
                    'endNode': endNode,
                    'time_travelled': time_travelled,
                    'dist': dist,
                    'closest_points': ListCoor
                })
                startNode = endNode
                numEdge += 1
                print(numEdge, dist)
                
        endTime = time.time()
        print(f"{endTime - startTime} seconds")
        
    def inputEdgesFromJSON(self, filename):
        with open(filename, 'r', encoding='utf8') as filein:
            for line in filein:
                edge = json.loads(line)
                self.Edges.append({'startNode': edge['startNode'], 
                                   'endNode': edge['endNode'], 
                                   'time_travelled': edge['time_travelled'], 
                                   'dist': edge['dist'], 
                                   'closest_points': edge['closest_points']
                                   })
    
    def inputGraphFromJSON(self, filename):
        self.inputEdgesFromJSON(filename)
        # adjacency list has form : {node_0: edges idx from node_0, node_1: edges idx from node_1,...}
        for edge_idx in range(len(self.Edges)):
            self.AdjList[self.Edges[edge_idx]['startNode']].append(edge_idx)

    def buildGraph(self, route_var_query, stop_query, path_query, stop_indices_dict):
        self.buildEdges(route_var_query, stop_query, path_query, stop_indices_dict)
        # adjacency list has form : {node_0: edges idx from node_0, node_1: edges idx from node_1,...}
        for edge_idx in range(len(self.Edges)):
            self.AdjList[self.Edges[edge_idx]['startNode']].append(edge_idx)
     
    def Dijkstra_with_trace(self, startNode):
        timeTaken = {}
        timeTaken[startNode] = 0
        pq = []
        heapq.heappush(pq, (0, startNode))
        visited = [False] * self.NumNodes
        
        predecessors = {}
        
        while pq:
            curNode_time, curNode = heapq.heappop(pq)
            
            if visited[curNode]:
                continue
            
            visited[curNode] = True
            
            for edge_idx in self.AdjList[curNode]:
                
                edge = self.Edges[edge_idx]
                if edge['endNode'] not in timeTaken:
                    timeTaken[edge['endNode']] = float('inf')
                newTime = curNode_time + edge['time_travelled']
                if newTime < timeTaken[edge['endNode']]:
                    timeTaken[edge['endNode']] = newTime
                    heapq.heappush(pq, (newTime, edge['endNode']))
                    predecessors[edge['endNode']] = curNode
        return (timeTaken, predecessors)
    
    def form_path(self, startNode, timeTaken, predecessors):
        paths = {}
        for idx in range(self.NumNodes):
            if idx in timeTaken and timeTaken[idx] != float('inf'):
                tmp = idx
                path = []
                while tmp != startNode:
                    path.append(tmp)
                    tmp = predecessors[tmp]
                path.append(startNode)
                paths[idx] = reversed(path)
        return paths
    
    def Dijkstra(self, startNode):
        timeTaken = {}
        timeTaken[startNode] = 0
        pq = []
        heapq.heappush(pq, (0, startNode))
        visited = [False] * self.NumNodes
        
        while pq:
            curNodeTime, curNode = heapq.heappop(pq)
            
            if visited[curNode]:
                continue
            
            visited[curNode] = True
            
            for edge_idx in self.AdjList[curNode]:
                
                edge = self.Edges[edge_idx]
                if edge['endNode'] not in timeTaken:
                    timeTaken[edge['endNode']] = float('inf')
                newTime = curNodeTime + edge['time_travelled']
                if newTime < timeTaken[edge['endNode']]:
                    timeTaken[edge['endNode']] = newTime
                    heapq.heappush(pq, (newTime, edge['endNode']))
        return timeTaken
    
    def DijkstraAllPairs(self, uniqueIds):
        run_time = 0
        for node in range(self.NumNodes):
            startTime = time.time()
            self.Dijkstra(node)
            run_time += time.time() - startTime
            print('dijkstra progress: {}/4396 edges'.format(node))
        print('Total run time: {}'.format(run_time))
    
    def ExportShortestPathAllPairs(self, uniqueIds, filename):
        with open(filename, 'w', encoding='utf8') as fout:
            for u in range(self.NumNodes):
                result = self.Dijkstra(u)
                print('dijkstra progress: {}/4396 edges'.format(u))
                for v in range(self.NumNodes):
                    if u != v and v in result:
                        json.dump((uniqueIds[u], uniqueIds[v], result[v]), fout, ensure_ascii=False)
                        fout.write('\n')
    
    def shortestPath2Stops(self, start_stop_id, end_stop_id, stop_list):
        stop_indices_dict = self.buildStopIdDict(stop_list)
        shortestDist = self.Dijkstra(stop_indices_dict[start_stop_id])
        print(f"{start_stop_id},{end_stop_id} : {shortestDist[end_stop_id]}")
        
    def findKtopStops(self, uniqueIds, stop_list, k=10):
        count = {x: 0 for x in range(self.NumNodes)}
        for node in range(self.NumNodes):
            time, trace = self.Dijkstra_with_trace(node)
            print('dijkstra progress: {}/4396 edges'.format(node))
            paths = self.form_path(node, time, trace)
            for endNode in paths:
                for node in paths[endNode]:
                    count[node] += 1
                    
        count_idx = []
        for idx in range(len(count)):
            count_idx.append((count[idx], idx))
            
        count_idx_sorted = sorted(count_idx, reverse=True)
        top_stops_list = []
        for idx in range(k):
            stopId = uniqueIds[count_idx_sorted[idx][1]]
            stops = StopQuery(stop_list).searchByStopId(stopId)
            stop = stops[0]
            top_stops_list.append(stop)
        return top_stops_list
    
