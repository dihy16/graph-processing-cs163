import osmium as osm
import collections
import json
import LLtoXY
import EdgeMatrix
import random

class OSMHandler(osm.SimpleHandler):
    def __init__(self, osm_file):
        osm.SimpleHandler.__init__(self)
        self.nodes_in_ways = set()
        self.nodes = {} 
        self.ways = {}
        self.relations = {}
        self.bus_trips = []
        
        self.node_in_way(osm_file)
        self.apply_file(osm_file)
        
        self.num_nodes = 0
        self.num_intersections = 0
        self.num_edges = 0
        self.intersections = []
        
        self.adj_list = collections.defaultdict(list)
        self.trans_adj_list = collections.defaultdict(list)
        
        self.is_intersection = {x: False for x in self.nodes}
        self.occurrence_in_way = {x: 0 for x in self.nodes}
        self.edge_map = {}
        self.edge_matrix = EdgeMatrix.EdgeMatrix()
        
    def node_in_way(self, osm_file):
        class WayHandler(osm.SimpleHandler):
            def __init__(self, handler):
                super().__init__()
                self.handler = handler
            
            def way(self, w):
                if 'highway' in w.tags:
                    for n in w.nodes:
                        self.handler.nodes_in_ways.add(n.ref)
        
        way_handler = WayHandler(self)
        way_handler.apply_file(osm_file)
        
    def node(self, n):
        if n.id in self.nodes_in_ways:
            self.nodes[n.id] = (n.location.lat, n.location.lon)

    def way(self, w):
        if 'highway' in w.tags:
            node_ids = [n.ref for n in w.nodes]
            self.ways[w.id] = node_ids
            
    def relation(self, r):
        members = [(m.type, m.ref, m.role) for m in r.members]
        self.relations[r.id] = members

    def count_node_occurrence(self):
        for id in self.ways:
            way = self.ways[id]
            for i in range(len(way)):
                self.occurrence_in_way[way[i]] += 1

    def input_bus_trips(self, filename):
        with open(filename, 'r', encoding='utf8') as filein:
            for line in filein:
                query = json.loads(line)
                for trip in query['tripList']:
                    path = []
                    for pair in trip['edgesOfPath2']:
                        u, v = pair
                        u = int(u)
                        v = int(v)
                        if not self.is_intersection[u] and u in self.edge_map and (len(path) == 0 or self.edge_map[u] != path[-1]):
                            path.append(self.edge_map[u])
                        if not self.is_intersection[v] and v in self.edge_map and (len(path) == 0 or self.edge_map[v] != path[-1]):
                            path.append(self.edge_map[v])
                    if (len(path) > 0):
                        self.bus_trips.append(path)
                        self.edge_matrix.update_edge(path[0], path[-1], path)
                    
    
    def identify_intersections(self):
        for node in self.occurrence_in_way:
            if self.occurrence_in_way[node] > 1:
                self.is_intersection[node] = True
                self.intersections.append(node)
                self.num_intersections += 1
    
    def build_intersection_graph(self):
        edge_id = 0
        for way_id, way in self.ways.items():
            start_node = None
            path_nodes = []

            for node in way:
                if self.is_intersection[node]:
                    if start_node is not None:
                        self.adj_list[start_node].append((node, way_id, path_nodes.copy(), edge_id))
                        self.trans_adj_list[node].append((start_node, way_id, path_nodes.copy()[::-1], edge_id))
                        edge_id += 1
                    start_node = node
                    path_nodes = []
                elif start_node is not None:
                    path_nodes.append(node)
                    self.edge_map[node] = edge_id
        self.num_edges = edge_id
     
    def set_up(self, bus_trip_file):
        self.count_node_occurrence()
        self.identify_intersections()
        self.build_intersection_graph()
        self.num_nodes = len(self.nodes)
        self.input_bus_trips(bus_trip_file)

                
handler = OSMHandler('data/HoChiMinh.osm')
bus_trip_file = 'data/bus-history.json'
handler.set_up(bus_trip_file)
print('num intersections: ', handler.num_intersections)
print('num edges: ', handler.num_edges)
print('num nodes: ', handler.num_nodes)
print('num ways:', len(handler.ways))

edge_list = random.sample(range(0, handler.num_edges), 10000)
with open('data/edge_matrix.txt', 'w') as f:
    for edge in edge_list:
        if edge not in handler.edge_matrix.edge_matrix:
            continue
        f.write(f"Start: {edge} \n")
        for end in handler.edge_matrix.edge_matrix[edge]:
            if end not in handler.edge_matrix.edge_matrix[edge]:
                continue
            f.write(f"       End: {end} Edge {handler.edge_matrix.edge_matrix[edge][end].max_edge}\n")
            
d = handler.edge_matrix.to_dict()
with open('data/edge_matrix.json', 'w') as f:
    json.dump(d, f)



    




