from collections import defaultdict
from StopQuery import StopQuery
from PathQuery import PathQuery
import heapq
import json
import LLtoXY
import math
import copy

class Graph:
    INF = float('inf')

    def __init__(self, NumNodes):
        self.AdjList = defaultdict(list)
        self.TransAdjList = defaultdict(list)
        self.NumNodes = NumNodes
        self.NumEdges = 0
        self.MaxOutgoing = [0] * NumNodes  # MaxOutgoing[u] is the weight of the heaviest outgoing edge from u
        self.MinOutgoing = [self.INF] * NumNodes
        self.MaxIncoming = [0] * NumNodes
        
    def findDistBetween2Stops(self, minDistIdx, pathLngList, pathLatList, curStop):
        y_stop, x_stop = LLtoXY.convertLngLatToXY(curStop.getLng(), curStop.getLat())    
        min_dist = self.INF
        for j1 in range(minDistIdx, len(pathLngList)):
            y1, x1 = LLtoXY.convertLngLatToXY(pathLngList[j1], pathLatList[j1])
            curDist = math.sqrt((x1 - x_stop) ** 2 + (y1 - y_stop) ** 2)
            if curDist < min_dist:
                min_dist = curDist
                ind = j1
                        
        path_points = []
        path_points.append((pathLatList[minDistIdx], pathLngList[minDistIdx]))
                
        dist = 0
        for idx in range(minDistIdx, ind):
            y1, x1 = LLtoXY.convertLngLatToXY(pathLngList[idx], pathLatList[idx])
            y2, x2 = LLtoXY.convertLngLatToXY(pathLngList[idx + 1], pathLatList[idx + 1])
            dist += LLtoXY.getDistance(x1, y1, x2, y2)
            path_points.append((pathLatList[idx + 1], pathLngList[idx + 1])) 
            
        return dist, ind, path_points
    
    def buildGraph(self, route_var_query, stop_query, path_query, stop_indices_dict):
        """Initialize list of edges for the graph from 3 lists: routeVars, stops, and paths"""
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
                
                dist, minDistIdx, path_points = self.findDistBetween2Stops(minDistIdx, pathLngList, pathLatList, curStop)
                
                time_travelled = dist / speed
                edge = (startNode, endNode, time_travelled, dist, path_points)
                self.addEdge(edge)
                
                startNode = endNode
                numEdge += 1
                
        self.NumEdges = numEdge
        
    def inputEdgesFromJSON(self, filename):
        numEdges = 0
        with open(filename, 'r', encoding='utf8') as filein:
            for line in filein:
                edge = json.loads(line)
                numEdges += 1
                edge = (edge['startNode'], edge['endNode'], edge['time_travelled'], edge['dist'], edge['path_points'])
                self.addEdge(edge)
        self.NumEdges = numEdges
                
    def outputEdgesAsJSON(self, filename):
        keys = ['startNode', 'endNode', 'time_travelled', 'dist', 'path_points']
        with open(filename, 'w', encoding='utf8') as fout:
            for u in range(self.NumNodes):
                edges = self.AdjList[u]
                for edge in edges:
                    edge_dict = {keys[i]: edge[i] for i in range(len(keys))}
                    json.dump(edge_dict, fout, ensure_ascii=False)
                    fout.write('\n')
    
    def addEdge(self, edge):
        self.AdjList[edge[0]].append(edge)
            
        transEdge = list(copy.deepcopy(edge))
        transEdge[0], transEdge[1] = transEdge[1], transEdge[0]
        self.TransAdjList[transEdge[0]].append(tuple(transEdge))
            
        w = edge[2]
        if self.MaxIncoming[edge[1]] < w:
            self.MaxIncoming[edge[1]] = w
            
        if self.MaxOutgoing[edge[0]] < w:
            self.MaxOutgoing[edge[0]] = w
            
        if self.MinOutgoing[edge[0]] > w:
            self.MinOutgoing[edge[0]] = w
   
    def relax_edges_from_node(self, curNode, pq, timeTaken, node_time, isTrans):
        for edge in self.TransAdjList[curNode] if isTrans else self.AdjList[curNode]:
            if edge[1] not in timeTaken:
                timeTaken[edge[1]] = self.INF
                
            if timeTaken[edge[1]] > node_time + edge[2]:
                timeTaken[edge[1]] = node_time + edge[2]
                heapq.heappush(pq, (node_time + edge[2], edge[1]))  
                
    def Dijkstra_1_Pair(self, startNode, goalNode):
        timeTaken = {x: self.INF for x in range(self.NumNodes)}
        timeTaken[startNode] = 0
        pq = []
        heapq.heappush(pq, (0, startNode))
        visited = [False] * self.NumNodes
    
        while pq:
            curNodeTime, curNode = heapq.heappop(pq)
            
            if curNode == goalNode:
                break
            if visited[curNode]:
                continue
            visited[curNode] = True
            self.relax_edges_from_node(curNode, pq, timeTaken, curNodeTime, False)
        if timeTaken[goalNode] != self.INF:
            return timeTaken[goalNode]
        return -1

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
            
            for edge in self.AdjList[curNode]:
                
                if edge[1] not in timeTaken:
                    timeTaken[edge[1]] = self.INF
                newTime = curNode_time + edge[2]
                if newTime < timeTaken[edge[1]]:
                    timeTaken[edge[1]] = newTime
                    heapq.heappush(pq, (newTime, edge[1]))
                    predecessors[edge[1]] = curNode
        return (timeTaken, predecessors)
    
    def form_path(self, startNode, timeTaken, predecessors):
        paths = {}
        for idx in range(self.NumNodes):
            if idx in timeTaken and timeTaken[idx] != self.INF:
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
            self.relax_edges_from_node(curNode, pq, timeTaken, curNodeTime, False)
            
        return timeTaken
    
    def DijkstraAllPairs(self):
        for node in range(self.NumNodes):
            self.Dijkstra(node)
    
    def ExportShortestPathAllPairs(self, uniqueIds, filename):
        with open(filename, 'w', encoding='utf8') as fout:
            for u in range(self.NumNodes):
                result = self.Dijkstra(u)
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
 
    def Bidirectional_Dijkstra(self, startNode, goalNode):
        timeF = {}
        timeF[startNode] = 0
        timeB = {}
        timeB[goalNode] = 0

        pq = []
        heapq.heappush(pq, (0, startNode))
        pq_rev = []
        heapq.heappush(pq_rev, (0, goalNode))

        
        visitedF = [False] * self.NumNodes
        visitedB = [False] * self.NumNodes
        
        best_dist = self.INF

        while pq or pq_rev:

            if pq:
                u_time, u = heapq.heappop(pq)
                
                if timeF[u] <= best_dist:
                    self.relax_edges_from_node(u, pq, timeF, u_time, False)
                    
                visitedF[u] = True
                if visitedB[u] and timeF[u] + timeB[u] < best_dist:
                    best_dist = timeF[u] + timeB[u]

            if pq_rev:
                u_time, u = heapq.heappop(pq_rev)
                
                if timeB[u] <= best_dist:
                    self.relax_edges_from_node(u, pq_rev, timeB, u_time, True)
                    
                visitedB[u] = True
                if visitedF[u] and timeF[u] + timeB[u] < best_dist:
                    best_dist = timeF[u] + timeB[u]

        if best_dist != self.INF:
            return best_dist
        return -1
   