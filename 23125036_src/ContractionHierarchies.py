import heapq
from re import L

class Shortcut:
    INF = float('inf')
    def __init__(self, f, t, d):
        self.from_node = f
        self.to_node = t
        self.dist = d

class ContractionHierarchies:
    INF = float('inf')
    def __init__(self, graph):
        self.is_adding_shortcuts = False
        self.n = graph.NumNodes
        self.rank = [self.INF] * self.n
        self.node_level = [0] * self.n
        self.settled_vertices = []
        self.shortcuts = []
        self.G = graph
        self.importance_queue = []
        self.dist = [self.INF] * self.n

    def update_neighbors_node_level(self, v):
        #print('start update neighbor')
        outgoing_edges = self.G.AdjList[v]
        incoming_edges = self.G.TransAdjList[v]
        current_v_level = self.node_level[v] + 1

        for idx in outgoing_edges:
            neighbor = self.G.Edges[idx]['endNode']
            if self.node_level[neighbor] < current_v_level:
                self.node_level[neighbor] = current_v_level

        for idx in incoming_edges:
            neighbor = self.G.Edges[idx]['startNode']
            if self.node_level[neighbor] < current_v_level:
                self.node_level[neighbor] = current_v_level
        #print('end update neighbor')

    def sum_contracted_neighbors_and_node_level(self, v):
        #print('start sum')
        num = 0
        level = 0

        outgoing_edges = self.G.AdjList[v]
        incoming_edges = self.G.TransAdjList[v]

        for idx in outgoing_edges:
            neighbor = self.G.Edges[idx]['endNode']
            if neighbor == v:
                print('False')
            if self.rank[neighbor] != self.INF:
                num += 1
                if self.node_level[neighbor] > level:
                    level = self.node_level[neighbor]

        for idx in incoming_edges:
            neighbor = self.G.Edges[idx]['startNode']
            if neighbor == v:
                print('False')
            if self.rank[neighbor] != self.INF:
                num += 1
                if self.node_level[neighbor] > level:
                    level = self.node_level[neighbor]
       # print('end sum')
        return num + level + 1

    def witness_search(self, source, v, limit):
        #print('start witness')
        queue = []
        heapq.heappush(queue, (0, source))
        self.settled_vertices.append(source)
        self.dist[source] = 0

        hops = 5

        while hops and queue:
            hops -= 1
            u = heapq.heappop(queue)[1]

            if limit < self.dist[u]:
                break

            for edge_idx in self.G.AdjList[u]:
                neighbour = self.G.Edges[edge_idx]['endNode']
                if (neighbour == u):
                    print('False')
                weight = self.G.Edges[edge_idx]['time_travelled']
                
                if (self.rank[neighbour] < self.rank[v]) or (neighbour == v):
                    continue

                if self.dist[neighbour] > self.dist[u] + weight:
                    self.dist[neighbour] = self.dist[u] + weight
                    heapq.heappush(queue, (self.dist[u] + weight, neighbour))
                    self.settled_vertices.append(neighbour)
       # print('end witness')
                    
    def contract_node(self, v):
        self.shortcuts = []

        added_shortcuts = 0
        shortcut_cover = 0

        outgoing_edges = self.G.AdjList[v]
        incoming_edges = self.G.TransAdjList[v]

        for idx in incoming_edges:
            u = self.G.Edges[idx]['startNode']
            if (u == v):
                print('False')
            timeU = self.G.Edges[idx]['time_travelled']
            if (self.rank[u] < self.rank[v]) or (not outgoing_edges):
                continue

            self.witness_search(u, v, self.G.max_incoming[v] + self.G.max_outgoing[v])

            at_least_one_shortcut = False

            for idx2 in outgoing_edges:   
                w = self.G.Edges[idx2]['endNode']
                if (w == v):
                    print('False')
                timeW = self.G.Edges[idx2]['time_travelled']
                if (self.rank[w] < self.rank[v]) or (w == u):
                    continue

                is_shortcut_needed = True

                for idx3 in self.G.TransAdjList[w]:
                    x = self.G.Edges[idx3]['startNode']
                    if (x == w):
                        print('False')
                    timeX = self.G.Edges[idx3]['time_travelled']
                    if (self.rank[x] < self.rank[v]) or (x == v):
                        continue

                    if timeU + timeW >= self.dist[x] + timeX:
                        is_shortcut_needed = False
                        break

                if is_shortcut_needed:
                    added_shortcuts += 1
                    at_least_one_shortcut = True

                if self.is_adding_shortcuts:    
                    distUV = self.G.Edges[idx]['dist']
                    pathUV = self.G.Edges[idx]['closest_points']
                    distVW = self.G.Edges[idx2]['dist']
                    pathVW = self.G.Edges[idx2]['closest_points']
              
                    self.shortcuts.append({'startNode': u,
                                            'endNode': w,
                                            'time_travelled': timeU + timeW,
                                            'dist': distUV + distVW,
                                            'closest_points': pathUV + pathVW
                                        })

            if at_least_one_shortcut:
                shortcut_cover += 1

            for x in self.settled_vertices:
                self.dist[x] = self.INF

            self.settled_vertices = []

        return (
            added_shortcuts - len(outgoing_edges) - len(incoming_edges)
            + shortcut_cover + self.sum_contracted_neighbors_and_node_level(v)
        )  
    """
    def contract_node(self, v):
        self.shortcuts = []
        added_shortcuts = 0
        shortcut_cover = 0

        outgoing_edges = self.G.AdjList[v]
        incoming_edges = self.G.TransAdjList[v]

        for idx in incoming_edges:
            u = self.G.Edges[idx]['startNode']
            time_u_to_v = self.G.Edges[idx]['time_travelled']
            u_idx = idx
            
            if self.rank[u] < self.rank[v] or not outgoing_edges:
                continue

            self.witness_search(u, v, self.G.max_incoming[v] + self.G.max_outgoing[v])

            at_least_one_shortcut = False

            for edgeIdx in outgoing_edges:
                w = self.G.Edges[edgeIdx]['endNode']
                time_v_to_w = self.G.Edges[edgeIdx]['time_travelled']
                w_idx = edgeIdx
                if self.rank[w] < self.rank[v]:
                    continue

                is_shortcut_needed = True
                cntx = 0
                for x_idx in self.G.TransAdjList[w]:
                    cntx += 1
                    x = self.G.Edges[x_idx]['startNode']
                    dist_x_to_w = self.G.Edges[x_idx]['time_travelled']
                    if self.rank[x] < self.rank[v] or x == v:
                        continue

                    # if dist(u,x,w) <= dist(u,v,w), no shortcut is needed
                    if self.dist[x] + dist_x_to_w <= time_u_to_v + time_v_to_w:
                        is_shortcut_needed = False
                        break
                    

                if is_shortcut_needed:
                    added_shortcuts += 1
                    at_least_one_shortcut = True

                    if self.is_adding_shortcuts:
                        dist_u_to_v = self.G.Edges[u_idx]['dist']
                        pathpoint_u_to_v = self.G.Edges[u_idx]['closest_points']
                        
                        dist_v_to_w = self.G.Edges[w_idx]['dist']
                        pathpoint_v_to_w = self.G.Edges[w_idx]['closest_points']
                        
                        self.shortcuts.append({'startNode': u,
                                               'endNode': w,
                                              'time_travelled': time_u_to_v + time_v_to_w,
                                             'dist': dist_u_to_v + dist_v_to_w,
                                            'closest_points': pathpoint_u_to_v + pathpoint_v_to_w
                                            })

            if at_least_one_shortcut:
                shortcut_cover += 1

            for x in self.settled_vertices:
                self.dist[x] = self.INF
            self.settled_vertices = []

        return added_shortcuts - len(outgoing_edges) - len(incoming_edges) + shortcut_cover + self.sum_contracted_neighbors_and_node_level(v)
    """
    
    def remove_edges(self):
        print('start remove')
        for i in range(self.n):
            j = 0
            while j < len(self.G.AdjList[i]):
                v = self.G.Edges[self.G.AdjList[i][j]]['endNode']
                if self.rank[i] > self.rank[v]:
                    self.G.AdjList[i].pop(j)
                else:
                    j += 1

        for i in range(self.n):
            j = 0
            while j < len(self.G.TransAdjList[i]):
                v = self.G.Edges[self.G.TransAdjList[i][j]]['startNode']
                if self.rank[i] > self.rank[v]:
                    self.G.TransAdjList[i].pop(j)
                else:
                    j += 1
        print('end remove')
                    
    def initialize_nodes_queue(self):
        print('start init queue')
        cntNeg = 0
        for v in range(self.n):
            #v = self.G.Edges[idx]['startNode']
            importance = self.contract_node(v)  
            if importance < 0:
                cntNeg += 1
                print(importance)
            heapq.heappush(self.importance_queue, (importance, v))
        print('end init queue, {}/{}'.format(cntNeg, self.n))

    def preprocess_graph(self):
        self.initialize_nodes_queue()
        # self.is_adding_shortcuts = True
        # rank_count = 0
        # while self.importance_queue:
        #     v = heapq.heappop(self.importance_queue)[1]
        #     importance = self.contract_node(v)
                
        #     if (not self.importance_queue) or (importance <= self.importance_queue[0][0]):
        #         for shortcut in self.shortcuts:
        #             self.G.Edges.append(shortcut)
        #             self.G.AdjList[shortcut['startNode']].append(len(self.G.Edges) - 1)
        #             self.G.TransAdjList[shortcut['endNode']].append(len(self.G.Edges) - 1)
                    
        #             w = shortcut['time_travelled']
            
        #             if self.G.max_incoming[shortcut['endNode']] < w:
        #                 self.G.max_incoming[shortcut['endNode']] = w
                
        #             if self.G.max_outgoing[shortcut['startNode']] < w:
        #                 self.G.max_outgoing[shortcut['startNode']] = w
                
        #             if self.G.min_outgoing[shortcut['startNode']] > w:
        #                 self.G.min_outgoing[shortcut['startNode']] = w

        #         self.update_neighbors_node_level(v)
        #         self.rank[v] = rank_count
        #         if rank_count < 0:
        #             print('rank_count: ', rank_count)
        #     else:
        #         heapq.heappush(self.importance_queue, (importance, v))
                
        #     rank_count += 1

        # self.remove_edges()
        

