import heapq

class ContractionHierarchies:
    INF = float('inf')
    def __init__(self, graph):
        self.num_nodes = graph.num_nodes
        self.G = graph
        self.is_init_queue = True
        self.rank = [self.INF] * self.num_nodes
        self.node_level = [0] * self.num_nodes
        self.dist = [self.INF] * self.num_nodes
        self.settled_vertices = []
        self.shortcuts = []
        self.importance_queue = []
        self.shortcuts_for_GeoJSON = []
        
    def update_neighbors_node_level(self, v):
        outgoing_edges = self.G.adj_list[v]
        incoming_edges = self.G.trans_adj_list[v]

        current_v_level = self.node_level[v] + 1

        for edge in outgoing_edges:
            if self.node_level[edge[1]] < current_v_level:
                self.node_level[edge[1]] = current_v_level
                
        for edge in incoming_edges:
            if self.node_level[edge[1]] < current_v_level:
                self.node_level[edge[1]] = current_v_level
                    
    def sum_contracted_neighbors_and_node_level(self, v):
        num = 0
        level = 0
      
        outgoing_edges = self.G.adj_list[v]
        incoming_edges = self.G.trans_adj_list[v]

        for edge in outgoing_edges:
            if self.rank[edge[1]] != self.INF:
                num += 1
                level = max(level, self.node_level[edge[1]])

        for edge in incoming_edges:
            if self.rank[edge[1]] != self.INF:
                num += 1
                level = max(level, self.node_level[edge[1]])

        return num + level + 1
   
    def witness_search(self, source, v, limit):
        queue = []  
        heapq.heappush(queue,(0, source))
        self.settled_vertices.append(source)

        self.dist[source] = 0
        while queue:
            u = heapq.heappop(queue)[1]

            if limit < self.dist[u]:
                break

            outgoing_edges = self.G.adj_list[u]
            for edge in outgoing_edges:
                w = edge[1]
                weight = edge[2]
                if self.rank[w] < self.rank[v] or w == v:
                    continue

                if self.dist[w] > self.dist[u] + weight:
                    self.dist[w] = self.dist[u] + weight
                    heapq.heappush(queue,(self.dist[w], w))
                    self.settled_vertices.append(w)
                    
    def contract_node(self, v):
        self.shortcuts = []

        outgoing_edges = self.G.adj_list[v]
        incoming_edges = self.G.trans_adj_list[v]
        
        num_shortcuts = 0
        shortcut_cover = 0
       
        for incoming_edge in incoming_edges:
            if self.rank[incoming_edge[1]] < self.rank[v] or not outgoing_edges:
                continue

            self.witness_search(incoming_edge[1], v, self.G.max_incoming[v] + self.G.max_outgoing[v])
            
            need_shortcut = False
            for outgoing_edge in outgoing_edges:
                if self.rank[outgoing_edge[1]] < self.rank[v] or incoming_edge[1] == outgoing_edge[1]:
                    continue

                if self.dist[outgoing_edge[1]] > incoming_edge[2] + outgoing_edge[2]:
                    num_shortcuts += 1
                    need_shortcut = True
                    if not self.is_init_queue:
                        is_new_shortcut = True
                        # dist_u = incoming_edge[3]
                        # path_points_u = incoming_edge[4]
                        # dist_w = outgoing_edge[3]
                        # path_points_w = outgoing_edge[4]
                        
                        # for i in range(len(self.shortcuts)):
                        #     if u != self.shortcuts[i][0] or w != self.shortcuts[i][1]:
                        #         continue
                        #     is_new_shortcut = False
                        #     if self.shortcuts[i][2] > weight_u + weight_w:
                        #         self.shortcuts[i] = (u, w, weight_u + weight_w, dist_u + dist_w, path_points_u + path_points_w)
                        # if is_new_shortcut:
                        #     self.shortcuts.append((u, w, weight_u + weight_w, dist_u + dist_w, path_points_u + path_points_w))
                        for i, shortcut in enumerate(self.shortcuts):
                            if incoming_edge[1] == shortcut[0] and outgoing_edge[1] == shortcut[1]:
                                is_new_shortcut = False
                                if shortcut[2] > incoming_edge[2] + outgoing_edge[2]:
                                    self.shortcuts[i] = (incoming_edge[1], outgoing_edge[1], incoming_edge[2] + outgoing_edge[2], incoming_edge[3] + outgoing_edge[3], incoming_edge[4] + outgoing_edge[4])
                                break
                        if is_new_shortcut:
                            self.shortcuts.append((incoming_edge[1], outgoing_edge[1], incoming_edge[2] + outgoing_edge[2], incoming_edge[3] + outgoing_edge[3], incoming_edge[4] + outgoing_edge[4]))
            
            if need_shortcut:
                shortcut_cover += 1
            for visited_node in self.settled_vertices:
                self.dist[visited_node] = self.INF
            self.settled_vertices = []
        importance = num_shortcuts - len(incoming_edges) - len(outgoing_edges) + shortcut_cover + self.sum_contracted_neighbors_and_node_level(v) 
        return importance
    
    def remove_edges(self):
        for i in range(self.num_nodes):
            j = 0
            s = len(self.G.adj_list[i])
            while j < s:
                v = self.G.adj_list[i][j][1]
                if self.rank[i] > self.rank[v]:
                    del self.G.adj_list[i][j]
                    s -= 1
                else:
                    j += 1

            j = 0
            s = len(self.G.trans_adj_list[i])
            while j < s:
                v = self.G.trans_adj_list[i][j][1]
                if self.rank[i] > self.rank[v]:
                    del self.G.trans_adj_list[i][j]
                    s -= 1
                else:
                    j += 1
                
    def initialize_nodes_queue(self):
        for v in range(self.num_nodes):
            importance = self.contract_node(v)  
            heapq.heappush(self.importance_queue, (importance, v))

    def preprocess_graph(self):
        self.initialize_nodes_queue()
        
        self.is_init_queue = False
        rank_count = 0
        while self.importance_queue:
            v = heapq.heappop(self.importance_queue)[1]
            importance = self.contract_node(v)
                
            if not self.importance_queue or importance <= self.importance_queue[0][0]:
                for shortcut in self.shortcuts:
                    self.G.add_edge(shortcut)
                    self.shortcuts_for_GeoJSON.append(shortcut)
                self.update_neighbors_node_level(v)
                self.rank[v] = rank_count
            else:
                heapq.heappush(self.importance_queue, (importance, v))
                
            rank_count += 1
        
        self.remove_edges()
        
    def exportShortcutsToGeoJSON(self):
        pass
    
    def exportShorcutsToFile(self):
        pass
        

