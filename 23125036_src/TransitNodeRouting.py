import heapq

class TransitNodeRouting:
    INF = float('inf')
    def __init__(self, graph, rank):
        self.graph = graph
        self.num_nodes = graph.num_nodes
        self.is_transit = [False for _ in range(self.num_nodes)]
        self.transit_nodes = []
        self.rank = rank
        self.TNR_dist = {}
        self.Voronoi_Id = [-1 for _ in range(self.num_nodes)]
        self.adj_list = [[] for _ in range(self.num_nodes)]
        self.trans_adj_list = [[] for _ in range(self.num_nodes)]

        self.forward_search_space = [{} for _ in range(self.num_nodes)]
        self.forward_access_node_dist = [{} for _ in range(self.num_nodes)]
        self.forward_TNRed = [False for _ in range(self.num_nodes)]
        
        self.backward_search_space = [{} for _ in range(self.num_nodes)]
        self.backward_access_node_dist = [{} for _ in range(self.num_nodes)]
        self.backward_TNRed = [False for _ in range(self.num_nodes)]
        
    def build_adj_list(self):
        for edge in self.graph.edges:
            self.adj_list[edge[0]].append((edge[0], edge[1], edge[2], edge[3], edge[4]))
            self.trans_adj_list[edge[1]].append((edge[1], edge[0], edge[2], edge[3], edge[4]))
            
    #def save_tnr_to_file(self):
        
        
    def compute_TNR(self, num_transits, uniqueIds):
        if num_transits > self.num_nodes:
            print('Too many transit nodes')
            return
        self.build_adj_list()
        self.select_transit_nodes(num_transits)
        self.build_distance_table(uniqueIds)
        self.build_Voronoi_regions()
        self.compute_local_filter(uniqueIds)
        
    def select_transit_nodes(self, num_transits):
        for x in range(self.graph.num_nodes):    
            if len(self.transit_nodes) == num_transits:
                break
            if self.rank[x] >= self.num_nodes - num_transits:
                self.is_transit[x] = True
                self.transit_nodes.append(x)
        print('Num transit nodes: ', len(self.transit_nodes))
            
    def build_distance_table(self, uniqueIds):
        for x in self.transit_nodes:
            if x not in self.TNR_dist:
                self.TNR_dist[x] = {}
            for y in self.transit_nodes:
                if x == y:
                    self.TNR_dist[x][y] = (0, [], [])
                else:
                    self.TNR_dist[x][y] = self.graph.bidirectional_dijkstra(x, y, uniqueIds)
        # for x in range(num_transits):
        #     if self.transit_nodes[x] not in self.TNR_dist:
        #         self.TNR_dist[self.transit_nodes[x]] = {}
        #     for y in range(num_transits):
        #         if x == y:
        #             self.TNR_dist[self.transit_nodes[x]][self.transit_nodes[y]] = 0
        #         else:
        #             distance = self.graph.bidirectional_dijkstra(self.transit_nodes[x], self.transit_nodes[y])
        #             self.TNR_dist[self.transit_nodes[x]][self.transit_nodes[y]] = distance
                    
    def build_Voronoi_regions(self):
        distance_heap = []
        
        dist = [self.INF for _ in range(self.num_nodes)]
        
        for t_node in self.transit_nodes:
            dist[t_node] = 0
            self.Voronoi_Id[t_node] = t_node
            heapq.heappush(distance_heap, (0, t_node))
            
        visited = [False for _ in range(self.num_nodes)]
        
        while distance_heap:
            dist_v, v = heapq.heappop(distance_heap)
            if visited[v]:
                continue
            visited[v] = True
            
            for in_edge in self.trans_adj_list[v]:
                if dist_v + in_edge[2] < dist[in_edge[1]]:
                    dist[in_edge[1]] = dist_v + in_edge[2]
                    heapq.heappush(distance_heap, (dist[in_edge[1]], in_edge[1]))
                    self.Voronoi_Id[in_edge[1]] = self.Voronoi_Id[v]
                    
    def compute_local_filter(self, uniqueIds):
        contraction_max_heap = []
        for x in range(self.num_nodes):
            heapq.heappush(contraction_max_heap, (-self.rank[x], x))
            
        while contraction_max_heap:
            s = heapq.heappop(contraction_max_heap)[1]
            if not self.forward_TNRed[s]:
                self.forward_TNR(s, uniqueIds)
            if not self.backward_TNRed[s]:
                self.backward_TNR(s, uniqueIds)
                
    def forward_TNR(self, s, uniqueIds):
        search_heap = []
        heapq.heappush(search_heap, (0, s))
        
        distance = [self.INF for _ in range(self.num_nodes)]
        distance[s] = 0
        
        while search_heap:
            q = heapq.heappop(search_heap)[1]
            if q not in self.transit_nodes:
                self.forward_search_space[s][self.Voronoi_Id[q]] = True
                
                if self.forward_TNRed[q]:
                    for k in self.forward_search_space[q]:
                        self.forward_search_space[s][k] = True
                    for k in self.forward_access_node_dist[q]:
                        self.forward_access_node_dist[s][k] = -1
                else:
                    for out_edge in self.adj_list[q]:
                        if self.rank[q] < self.rank[out_edge[1]]: #check later
                            if distance[out_edge[1]] > distance[q] + out_edge[2]:
                                distance[out_edge[1]] = distance[q] + out_edge[2]
                                heapq.heappush(search_heap, (distance[out_edge[1]], out_edge[1]))
            else:
                self.forward_access_node_dist[s][q] = -1
                
        for k in self.forward_access_node_dist[s]:
            self.forward_access_node_dist[s][k] = self.graph.bidirectional_dijkstra(s, k, uniqueIds)
        
        access_node_mask = {}
        for k1 in self.forward_access_node_dist[s]:
            d1 = self.forward_access_node_dist[s][k1][0]
            for k2 in self.forward_access_node_dist[s]:
                d2 = self.forward_access_node_dist[s][k2][0]
                if k1 == k2:
                    continue
                if d1 + self.TNR_dist[k1][k2][0] <= d2:
                    access_node_mask[k2] = True
        
        for k in access_node_mask:
            del self.forward_access_node_dist[s][k]
            
        self.forward_TNRed[s] = True
        
    def backward_TNR(self, s, uniqueIds):
        search_heap = []
        heapq.heappush(search_heap, (0, s))
        
        distance = [self.INF for _ in range(self.num_nodes)]
        distance[s] = 0
        
        while search_heap:
            q = heapq.heappop(search_heap)[1]
            if q not in self.transit_nodes:
                self.backward_search_space[s][self.Voronoi_Id[q]] = True
                if self.backward_TNRed[q]:
                    for k in self.backward_search_space[q]:
                        self.backward_search_space[s][k] = True
                    for k in self.backward_access_node_dist[q]:
                        self.backward_access_node_dist[s][k] = -1
                else:
                    for in_edge in self.trans_adj_list[q]:
                        if self.rank[q] < self.rank[in_edge[1]]: #check later
                            if distance[in_edge[1]] > distance[q] + in_edge[2]:
                                distance[in_edge[1]] = distance[q] + in_edge[2]
                                heapq.heappush(search_heap, (distance[in_edge[1]], in_edge[1]))
                    
            else:
                self.backward_access_node_dist[s][q] = -1
                
        for k in self.backward_access_node_dist[s]:
            self.backward_access_node_dist[s][k] = self.graph.bidirectional_dijkstra(k, s, uniqueIds)
        
        access_node_mask = {}
        for k1 in self.backward_access_node_dist[s]:
            d1 = self.backward_access_node_dist[s][k1][0]
            for k2 in self.backward_access_node_dist[s]:
                if k1 == k2:
                    continue
                d2 = self.backward_access_node_dist[s][k2][0]
                if d1 + self.TNR_dist[k2][k1][0] <= d2:
                    access_node_mask[k2] = True
        
        for k in access_node_mask:
            del self.backward_access_node_dist[s][k]
            
        self.backward_TNRed[s] = True
        
    def shortest_path(self, s, t, uniqueIds):
        dist, path, coors = self.TNR_shortest_path(s, t)
        if dist > 0:
            return 1, dist, path, coors
        new_dist, path, coors = self.graph.bidirectional_dijkstra(s, t, uniqueIds)
        if dist == -1:
            return -1, new_dist, path, coors
        return 0, new_dist, path, coors
        
    def TNR_shortest_path(self, s, t):
        if len(self.forward_access_node_dist[s]) == 0 or len(self.backward_access_node_dist[t]) == 0:
            return -1, [], []
        for k in self.forward_search_space[s]:
            if k in self.backward_search_space[t]:
                return 0, [], []
        best_dist = self.INF
        best_s_access_node = None
        best_t_access_node = None
        
        for k1 in self.forward_access_node_dist[s]:
            d1 = self.forward_access_node_dist[s][k1][0]
            for k2 in self.backward_access_node_dist[t]:
                d2 = self.backward_access_node_dist[t][k2][0]
                if best_dist > d1 + self.TNR_dist[k1][k2][0] + d2:
                    best_dist = d1 + self.TNR_dist[k1][k2][0] + d2
                    best_s_access_node = k1
                    best_t_access_node = k2
                    
        if best_dist == self.INF:
            return -self.INF, [], []
        
        
        path = []
        coors = []
        if best_s_access_node and best_t_access_node:
            path.extend(self.forward_access_node_dist[s][best_s_access_node][1])
            path.extend(self.TNR_dist[best_s_access_node][best_t_access_node][1][1:])
            coors.extend(self.forward_access_node_dist[s][best_s_access_node][2])
            coors.extend(self.TNR_dist[best_s_access_node][best_t_access_node][2])
            path.extend(self.backward_access_node_dist[t][best_t_access_node][1][1:])
            coors.extend(self.backward_access_node_dist[t][best_t_access_node][2])
                            
        return best_dist, path, coors
        
   