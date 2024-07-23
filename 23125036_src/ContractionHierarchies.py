import heapq

class ContractionHierarchies:
    INF = float('inf')
    def __init__(self, graph):
        self.num_nodes = graph.NumNodes
        self.G = graph
        self.is_adding_shortcuts = False
        self.rank = [self.INF] * self.num_nodes
        self.node_level = [0] * self.num_nodes
        self.dist = [self.INF] * self.num_nodes
        self.settled_vertices = []
        self.shortcuts = []
        self.importance_queue = []

    def update_neighbors_node_level(self, v):
        outgoing_edges = self.G.AdjList[v]
        incoming_edges = self.G.TransAdjList[v]

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
      
        outgoing_edges = self.G.AdjList[v]
        incoming_edges = self.G.TransAdjList[v]

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
        self.settled_vertices.append(source);

        self.dist[source] = 0;


        while queue:
            u = heapq.heappop(queue)[1];

            if limit < self.dist[u]:
                break

            outgoing_edges = self.G.AdjList[u]
            for edge in outgoing_edges:
                w = edge[1]
                weight = edge[2]
                if self.rank[w] < self.rank[v] or w == v:
                    continue

                if self.dist[w] > self.dist[u] + weight:
                    self.dist[w] = self.dist[u] + weight
                    heapq.heappush(queue,(self.dist[w], w))
                    self.settled_vertices.append(w)
                    
    def contract_node(self, node):
        self.shortcuts = []

        outgoing_edges = self.G.AdjList[node]
        incoming_edges = self.G.TransAdjList[node]
        
        num_shortcuts = 0
        shortcut_cover = 0
       
        for in_edge in incoming_edges:
            if self.rank[in_edge[1]] < self.rank[node] or not outgoing_edges:
                continue

            self.witness_search(in_edge[1], node, self.G.MaxIncoming[node] + self.G.MaxOutgoing[node])
            
            shortcut_added = False
            for out_edge in outgoing_edges:

                if self.rank[out_edge[1]] < self.rank[node] or in_edge[1] == out_edge[1]:
                    continue

                if self.dist[out_edge[1]] > in_edge[2] + out_edge[2]:
                    num_shortcuts += 1
                    shortcut_added = True
                    if self.is_adding_shortcuts:
                        should_add = True
                        coor_path = in_edge[4].copy()
                        coor_path.extend(out_edge[4])
                        for i in range(len(self.shortcuts)):
                            if self.shortcuts[i][0] == in_edge[1] and self.shortcuts[i][1] == out_edge[1]:
                                if self.shortcuts[i][2] > in_edge[2] + out_edge[2]:
                                    self.shortcuts[i] = (in_edge[1], out_edge[1], in_edge[2] + out_edge[2], in_edge[3] + out_edge[3], coor_path)
                                should_add = False
                        if should_add:
                            self.shortcuts.append((in_edge[1], out_edge[1], in_edge[2] + out_edge[2], in_edge[3] + out_edge[3], coor_path))
            
            if shortcut_added:
                shortcut_cover += 1
            for visited_node in self.settled_vertices:
                self.dist[visited_node] = self.INF
            self.settled_vertices = []
        
        importance = num_shortcuts - len(incoming_edges) - len(outgoing_edges) + shortcut_cover + self.sum_contracted_neighbors_and_node_level(node) 
       
        return importance
    
    def remove_edges(self):
        for i in range(self.num_nodes):
            j = 0
            s = len(self.G.AdjList[i])
            while j < s:
                v = self.G.AdjList[i][j][1]
                if self.rank[i] > self.rank[v]:
                    del self.G.AdjList[i][j]
                    s -= 1
                else:
                    j += 1

            j = 0
            s = len(self.G.TransAdjList[i])
            while j < s:
                v = self.G.TransAdjList[i][j][1]
                if self.rank[i] > self.rank[v]:
                    del self.G.TransAdjList[i][j]
                    s -= 1
                else:
                    j += 1
                
                    
    def initialize_nodes_queue(self):
        for v in range(self.num_nodes):
            importance = self.contract_node(v)  
            heapq.heappush(self.importance_queue, (importance, v))

    def preprocess_graph(self):
        self.initialize_nodes_queue()
        
        self.is_adding_shortcuts = True
        rank_count = 0
        while self.importance_queue:
            v = heapq.heappop(self.importance_queue)[1]
            importance = self.contract_node(v)
                
            if (not self.importance_queue) or (importance <= self.importance_queue[0][0]):
                for shortcut in self.shortcuts:
                    self.G.addEdge(shortcut)
                self.update_neighbors_node_level(v)
                self.rank[v] = rank_count
            else:
                heapq.heappush(self.importance_queue, (importance, v))
                
            rank_count += 1
        
        self.remove_edges()
        

