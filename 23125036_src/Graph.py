from collections import defaultdict
from StopQuery import StopQuery
from PathQuery import PathQuery
import heapq
import json
import LLtoXY
import copy

class Graph:
    INF = float('inf')

    def __init__(self, num_nodes):
        self.adj_list = defaultdict(list)
        self.trans_adj_list = defaultdict(list)
        self.num_nodes = num_nodes
        self.num_edges = 0
        self.edges = []
        self.max_outgoing = [0] * num_nodes  # max_outgoing[u] is the weight of the heaviest outgoing edge from u
        self.min_outgoing = [self.INF] * num_nodes
        self.max_incoming = [0] * num_nodes
        self.shortcuts = []
        
    def find_dist_between_2_stops(self, minDistIdx, pathLngList, pathLatList, curStop):
        y_stop, x_stop = LLtoXY.convertLngLatToXY(curStop.getLng(), curStop.getLat())    
        min_dist = self.INF
        for j1 in range(minDistIdx, len(pathLngList)):
            y1, x1 = LLtoXY.convertLngLatToXY(pathLngList[j1], pathLatList[j1])
            curDist = LLtoXY.getDistance(x1, y1, x_stop, y_stop)
            if curDist < min_dist:
                min_dist = curDist
                ind = j1
                        
        path_points = []
        path_points.append((pathLngList[minDistIdx], pathLatList[minDistIdx]))
                
        dist = 0
        for idx in range(minDistIdx, ind):
            y1, x1 = LLtoXY.convertLngLatToXY(pathLngList[idx], pathLatList[idx])
            y2, x2 = LLtoXY.convertLngLatToXY(pathLngList[idx + 1], pathLatList[idx + 1])
            dist += LLtoXY.getDistance(x1, y1, x2, y2)
            path_points.append((pathLngList[idx + 1], pathLatList[idx + 1])) 
            
        return dist, ind, path_points
    
    def build_graph(self, route_var_query, stop_query, path_query, stop_indices_dict):
        """Initialize list of edges for the graph from 3 lists: routeVars, stops, and paths"""
        
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
                
                dist, minDistIdx, path_points = self.find_dist_between_2_stops(minDistIdx, pathLngList, pathLatList, curStop)
                time_travelled = dist / speed
                edge = (startNode, endNode, time_travelled, dist, path_points)
                self.add_edge(edge)
                startNode = endNode
        
    def input_edges_from_JSON(self, filename):
        num_edges = 0
        with open(filename, 'r', encoding='utf8') as filein:
            for line in filein:
                edge = json.loads(line)
                num_edges += 1
                edge = (edge['startNode'], edge['endNode'], edge['time_travelled'], edge['dist'], edge['path_points'])
                self.add_edge(edge)
        self.num_edges = num_edges
                
    def output_edges_as_JSON(self, filename):
        keys = ['startNode', 'endNode', 'time_travelled', 'dist', 'path_points']
        with open(filename, 'w', encoding='utf8') as fout:
            for u in range(self.num_nodes):
                edges = self.adj_list[u]
                for edge in edges:
                    edge_dict = {keys[i]: edge[i] for i in range(len(keys))}
                    json.dump(edge_dict, fout, ensure_ascii=False)
                    fout.write('\n')
    
    def add_edge(self, edge):
        self.num_edges += 1
        self.edges.append(tuple(edge))
        
        self.adj_list[edge[0]].append(edge)
            
        trans_edge = list(copy.deepcopy(edge))
        trans_edge[0], trans_edge[1] = trans_edge[1], trans_edge[0]
        self.trans_adj_list[trans_edge[0]].append(tuple(trans_edge))
            
        w = edge[2]
        if self.max_incoming[edge[1]] < w:
            self.max_incoming[edge[1]] = w
            
        if self.max_outgoing[edge[0]] < w:
            self.max_outgoing[edge[0]] = w
            
        if self.min_outgoing[edge[0]] > w:
            self.min_outgoing[edge[0]] = w
   
    def relax_edges_from_node(self, curNode, pq, timeTaken, node_time, isTrans):
        for edge in self.trans_adj_list[curNode] if isTrans else self.adj_list[curNode]:
            if edge[1] not in timeTaken:
                timeTaken[edge[1]] = self.INF
                
            if timeTaken[edge[1]] > node_time + edge[2]:
                timeTaken[edge[1]] = node_time + edge[2]
                heapq.heappush(pq, (node_time + edge[2], edge[1]))  
                
    def dijkstra_one_pair(self, start_node, goal_node):
        timeTaken = {}
        timeTaken[start_node] = 0
        pq = []
        heapq.heappush(pq, (0, start_node))
        visited = [False] * self.num_nodes
        while pq:
            curNodeTime, curNode = heapq.heappop(pq)
            
            if curNode == goal_node:
                break
            if visited[curNode]:
                continue
            visited[curNode] = True
            self.relax_edges_from_node(curNode, pq, timeTaken, curNodeTime, False)
        if goal_node in timeTaken:
            return timeTaken[goal_node]
        return -1

    def dijkstra_with_trace(self, start_node):
        timeTaken = {}
        timeTaken[start_node] = 0
        pq = []
        heapq.heappush(pq, (0, start_node))
        visited = [False] * self.num_nodes
        
        predecessors = {}
        
        while pq:
            curNode_time, curNode = heapq.heappop(pq)
            
            if visited[curNode]:
                continue
            
            visited[curNode] = True
            
            for edge in self.adj_list[curNode]:
                
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
        for idx in range(self.num_nodes):
            if idx in timeTaken and timeTaken[idx] != self.INF:
                tmp = idx
                path = []
                while tmp != startNode:
                    path.append(tmp)
                    tmp = predecessors[tmp]
                path.append(startNode)
                paths[idx] = path[::-1]
        return paths
   
    def dijkstra(self, start_node):
        timeTaken = {}
        timeTaken[start_node] = 0
        pq = []
        heapq.heappush(pq, (0, start_node))
        visited = [False] * self.num_nodes
        
        while pq:
            curNodeTime, curNode = heapq.heappop(pq)
            
            if visited[curNode]:
                continue
            visited[curNode] = True
            self.relax_edges_from_node(curNode, pq, timeTaken, curNodeTime, False)
            
        return timeTaken
    
    def dijkstra_all_pairs(self):
        for node in range(self.num_nodes):
            self.dijkstra(node)
    
    def export_dijkstra_all_pairs(self, uniqueIds, filename):
        with open(filename, 'w', encoding='utf8') as fout:
            for u in range(self.num_nodes):
                result = self.dijkstra(u)
                for v in range(self.num_nodes):
                    if u != v and v in result:
                        json.dump((uniqueIds[u], uniqueIds[v], result[v]), fout, ensure_ascii=False)
                        fout.write('\n')
    
    def dijkstra_one_pair_with_trace(self, start_node, goal_node):
        timeTaken = {x: self.INF for x in range(self.num_nodes)}
        timeTaken[start_node] = 0
        pq = []
        heapq.heappush(pq, (0, start_node))
        visited = [False] * self.num_nodes
        
        predecessors = {}
        coor_path = {}
        
        while pq:
            curNode_time, curNode = heapq.heappop(pq)
            
            if curNode == goal_node:
                break
            if visited[curNode]:
                continue
            for edge in self.adj_list[curNode]:
                newTime = curNode_time + edge[2]
                if newTime < timeTaken[edge[1]]:
                    timeTaken[edge[1]] = newTime
                    heapq.heappush(pq, (newTime, edge[1]))
                    predecessors[edge[1]] = curNode
                    coor_path[edge[1]] = edge[4]
                    
        if timeTaken[goal_node] != self.INF:
            return timeTaken[goal_node], predecessors, coor_path
        return -1, predecessors, coor_path
    
    def export_path_2_stops(self, start_node, goal_node, uniqueIds, stop_list, filename):
        time_taken, prev_nodes, coor_path = self.dijkstra_one_pair_with_trace(start_node, goal_node)
        
        if time_taken == self.INF:
            return
        
        path = []
        tmp = goal_node
        
        stop_query = StopQuery(stop_list)
        start_stop = stop_query.searchByStopId(uniqueIds[start_node])[0]
        end_stop = stop_query.searchByStopId(uniqueIds[goal_node])[0]
        
        coors = [[end_stop.getLng(), end_stop.getLat()]]
        stops = [[end_stop.getLng(), end_stop.getLat()]]
        while tmp != start_node:
            path.append(uniqueIds[tmp])
            coors.extend(coor_path[tmp][::-1])
            tmp = prev_nodes[tmp]
            stops.append([stop_query.searchByStopId(uniqueIds[tmp])[0].getLng(), stop_query.searchByStopId(uniqueIds[tmp])[0].getLat()])
            
        path.append(uniqueIds[start_node])
        path = path[::-1]
        
        coors.append([start_stop.getLng(), start_stop.getLat()])
        coors = coors[::-1]
        stops.append([start_stop.getLng(), start_stop.getLat()])
        stops = stops[::-1]
        
        LLtoXY.exportLineStringToGeoJSON(coors, stops, filename)
        return path, coors
      
    def find_k_top_stops(self, uniqueIds, stop_list, k=10):
        count = {x: 0 for x in range(self.num_nodes)}
        for node in range(self.num_nodes):
            time, trace = self.dijkstra_with_trace(node)
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
 
    def bidirectional_dijkstra(self, startNode, goalNode):
        timeF = {}
        timeF[startNode] = 0
        timeB = {}
        timeB[goalNode] = 0

        pq = []
        heapq.heappush(pq, (0, startNode))
        pq_rev = []
        heapq.heappush(pq_rev, (0, goalNode))

        
        visitedF = [False] * self.num_nodes
        visitedB = [False] * self.num_nodes
        
        best_dist = self.INF
        
        predecessors = {}
        coor_path = {}

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
   