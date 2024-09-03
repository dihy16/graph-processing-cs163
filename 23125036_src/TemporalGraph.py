from collections import defaultdict
import csv
import copy
import heapq

class Node:
    def __init__(self, route_id, var_id, stop_id, timestamp, latx, lngy):
        self.route_id = route_id
        self.var_id = var_id
        self.stop_id = stop_id
        self.timestamp = timestamp
        self.latx = latx
        self.lngy = lngy
    
    def __eq__(self, other):
        return (self.route_id, self.var_id, self.stop_id, self.timestamp, self.latx, self.lngy) == \
               (other.route_id, other.var_id, other.stop_id, other.timestamp, other.latx, other.lngy)

    def __hash__(self):
        return hash((self.route_id, self.var_id, self.stop_id, self.timestamp, self.latx, self.lngy))
    
    def __lt__(self, other):
        return (self.timestamp) < (other.timestamp)

class Graph:
    INF = float('inf')
    def __init__(self, filename1, filename2):
        self.adj_list = defaultdict(list)
        #self.trans_adj_list = defaultdict(list)
        self.num_nodes = 0
        self.num_edges = 0
        self.nodes = []
        self.edges = []
        self.map_vehicle_to_rv = {}
        self.stops_timestamps = {}
        # self.max_outgoing = [0] * num_nodes  # max_outgoing[u] is the weight of the heaviest outgoing edge from u
        # self.min_outgoing = [self.INF] * num_nodes
        # self.max_incoming = [0] * num_nodes
        # self.shortcuts = []
        self.read_edges(filename1, filename2)
        # self.isContracted = False
        # self.isTNRed = False
            
    def parse_weight(self, row):
        if row[20] == '1' or row[20] == '2':  
            num_transfers = 0
        elif row[20] == '3' or row[20] == '4':  
            num_transfers = 1
        travel_time = int(float(row[8])) 
        return (num_transfers, travel_time)
    
    def read_edges(self, filename1, filename2):
        nodes = set()
        self.input_from_CSV(filename1, nodes, True)
        self.input_from_CSV(filename2, nodes)
        self.nodes = list(nodes)
        self.num_nodes = len(self.nodes)
        
    def input_from_CSV(self, filename, nodes, isType12=False):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                node_depart = Node(route_id=row[1],
                                   var_id=row[2],
                                   stop_id=row[0],
                                   timestamp=int(float(row[3])),
                                   latx=float(row[9]),
                                    lngy=float(row[10]))
                
                
                node_arrival = Node(route_id=row[5],
                                   var_id=row[6],
                                   stop_id=row[4],
                                    timestamp=int(float(row[7])),
                                    latx=float(row[11]),
                                    lngy=float(row[12]))
                
                bus_depart = row[13]
                bus_arrival = row[14]
                
                weight = self.parse_weight(row)
                edge = (node_depart, node_arrival, weight, bus_depart, bus_arrival)
                nodes.add(node_depart)
                nodes.add(node_arrival)
                self.add_edge(edge)
                
                if isType12:
                    self.map_vehicle_to_rv[row[13]] = (row[1], row[2])
                    if row[0] not in self.stops_timestamps:
                        self.stops_timestamps[row[0]] = []
                    self.stops_timestamps[row[0]].append(node_depart)

    def add_edge(self, edge):
        self.edges.append(tuple(edge))
        new_edge = list(copy.deepcopy(edge))
        new_edge.append(self.num_edges)
        new_edge = new_edge[1:]
        self.num_edges += 1
        self.adj_list[edge[0]].append(tuple(new_edge))
            
        # trans_edge = list(copy.deepcopy(new_edge))
        # trans_edge[0], trans_edge[1] = trans_edge[1], trans_edge[0]
        # self.trans_adj_list[trans_edge[0]].append(tuple(trans_edge))
            
        # w = edge[2]
        # if self.max_incoming[edge[1]] < w:
        #     self.max_incoming[edge[1]] = w
            
        # if self.max_outgoing[edge[0]] < w:
        #     self.max_outgoing[edge[0]] = w
            
        # if self.min_outgoing[edge[0]] > w:
        #     self.min_outgoing[edge[0]] = w
        
    def build_path_1d(self, start_node, goal_node, prev_nodes):
        path = []
        timestamps = []
        tmp = goal_node
        while tmp != start_node:
            path.append(tmp.stop_id)
            timestamps.append(tmp.timestamp)
            tmp = prev_nodes[tmp]
        path.append(start_node.stop_id)
        timestamps.append(start_node.timestamp)
        return path[::-1], timestamps[::-1]

    def dijkstra_with_trace(self, start_node, node_id_list):
        timeTaken = {}
        timeTaken[start_node] = 0
        pq = []
        heapq.heappush(pq, (0, start_node))
        visited = [False] * self.num_nodes
        
        predecessors = {}
        
        while pq:
            # curNode = (num_transfer, node)
            curNode_time, curNode = heapq.heappop(pq)
            if visited[node_id_list[curNode]]:
                continue
            
            visited[node_id_list[curNode]] = True
            
            # self.adj_list[node_depart] = (node_arrival, (num_transfer, time dif), bus_depart, bus_arrival)
            for edge in self.adj_list[curNode]:
                if edge[0].timestamp < curNode.timestamp: #skip if timestamp not valid
                    continue
                
                # skip if not in the same route var 
                if (curNode.route_id, curNode.var_id) != self.map_vehicle_to_rv[edge[2]]:
                    continue
                
                if edge[0] not in timeTaken:
                    timeTaken[edge[0]] = self.INF
                    
                newTime = curNode_time + edge[1][1]
                if newTime < timeTaken[edge[0]]:
                    timeTaken[edge[0]] = newTime
                    heapq.heappush(pq, (newTime, edge[0]))
                    predecessors[edge[0]] = curNode
        return (timeTaken, predecessors)
                
    def dijkstra_one_pair_with_trace(self, start_node, goal_node):
        timeTaken = {}
        timeTaken[start_node] = (0, 0)
        pq = []
        heapq.heappush(pq, (0, start_node))
        visited = [False] * self.num_nodes
        
        predecessors = {}
        
        while pq:
            # curNode = (num_transfer, node)
            curNode_time, curNode = heapq.heappop(pq)
            if curNode == goal_node:
                break
            if visited[curNode]:
                continue
            
            visited[curNode] = True
            
            # self.adj_list[node_depart] = (node_arrival, (num_transfer, time dif), bus_depart, bus_arrival)
            
            for edge in self.adj_list[curNode[1]]:
                if edge[0].timestamp < curNode[1].timestamp: # skip if timestamp not valid
                    continue
                
                # skip if not in the same route var 
                if (curNode.route_id, curNode.var_id) != self.map_vehicle_to_rv[edge[2]]:
                    continue
                
                if edge[0] not in timeTaken:
                    timeTaken[edge[0]] = self.INF
                    
                newTime = curNode_time + edge[1][1]
                if newTime < timeTaken[edge[0]]:
                    timeTaken[edge[0]] = newTime
                    heapq.heappush(pq, (newTime, (edge[1][0], edge[0])))
                    predecessors[edge[0]] = curNode
        path = self.build_path_1d(start_node, goal_node, predecessors)
        return (timeTaken, path)

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

    # def find_k_top_stops(self, stop_list, k=10):
    #     count = {x: 0 for x in range(self.num_nodes)}
    #     for node in range(self.num_nodes):
    #         time, trace = self.dijkstra_with_trace(node)
    #         paths = self.form_path(node, time, trace)
    #         for endNode in paths:
    #             for node in paths[endNode]:
    #                 count[node] += 1
                    
    #     count_idx = []
    #     for idx in range(len(count)):
    #         count_idx.append((count[idx], idx))
            
    #     count_idx_sorted = sorted(count_idx, reverse=True)
    #     top_stops_list = []
    #     for idx in range(k):
    #         stopId = uniqueIds[count_idx_sorted[idx][1]]
    #         stops = StopQuery(stop_list).searchByStopId(stopId)
    #         stop = stops[0]
    #         top_stops_list.append(stop)
    #     return top_stops_list
    
    def build_node_id_list(self):
        node_id_list= {}
        for i in range(self.num_nodes):
            node_id_list[self.nodes[i]] = i
        return node_id_list

    
graph = Graph('data/type12.csv', 'data/type34.csv')
print(graph.num_nodes)
print(graph.num_edges)

node_id_list = graph.build_node_id_list()
start_stop = '7617'
end_stop = '1192'
time_list = []
path_list = []
timestamps_list = []

min_time = graph.INF
earliest_departure = graph.INF
earliest_arrival = graph.INF

best_trip = 0

for start_node in graph.stops_timestamps[start_stop]:
    time, predecessors = graph.dijkstra_with_trace(start_node, node_id_list)
    trip_id = 0
    for end_node in time:
        if end_node.stop_id == end_stop:
            path, timestamps = graph.build_path_1d(start_node, end_node, predecessors)
            time_list.append(time[end_node])
            path_list.append(path)
            timestamps_list.append(timestamps)
            if time_list[trip_id] < min_time:
                min_time = time_list[trip_id]
                best_trip = trip_id
            elif time_list[trip_id] == min_time:
                if earliest_departure > timestamps_list[trip_id][0]:
                    earliest_departure = timestamps_list[trip_id][0]
                    best_trip = trip_id
                elif earliest_departure == timestamps_list[trip_id][0]:
                    if earliest_arrival > timestamps_list[trip_id][-1]:
                        best_trip = trip_id
                        earliest_arrival = timestamps_list[trip_id][-1]
            trip_id += 1

test_file = 'data/testing.txt'
with open(test_file, 'w') as f:
    f.write(f"best trip: time: {time_list[best_trip]}, path: {path_list[best_trip]}, timestamps: {timestamps_list[best_trip]}\n")
    for i in range(len(time_list)):
        f.write(f"time: {time_list[i]}, path: {path_list[i]}, timestamps: {timestamps_list[i]}\n")
print('Success to ', test_file)
#k_top_stops = graph.find_k_top_stops(graph.nodes, 10)