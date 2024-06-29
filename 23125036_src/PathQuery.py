import csv
import json
from site import enablerlcompleter

from Path import Path

class PathQuery:
    def __init__(self, path_list):
        self.path_list = path_list
        
    def searchByLat(self, lat):
        lst = [path for path in self.path_list if path.getLat() == lat]
        return lst
    
    def searchByLng(self, lng):
        lst = [path for path in self.path_list if path.getLng() == lng]
        return lst
    
    def searchByRouteId(self, routeId):
        lst = [path for path in self.path_list if path.getRouteId() == routeId]
        return lst
    
    def searchByRouteVarId(self, routeVarId):
        lst = [path for path in self.path_list if path.getRouteVarId() == routeVarId]
        return lst

    def outputAsCSV(self, query_list, filename):
        with open(filename, 'w', encoding='utf8', newline='') as fileout:
            fieldnames = ['Lat', 'Lng', 'RouteId', 'RouteVarId']
            csv_writer = csv.DictWriter(fileout, fieldnames=fieldnames)
            csv_writer.writeheader()
            for query in query_list:
                csv_writer.writerow(query.__dict__)

    def outputAsJSON(self, query_list, filename):
        with open(filename, 'w', encoding='utf8') as fileout:
            for query in query_list:
                json.dump(query.__dict__, fileout, ensure_ascii=False)
                fileout.write('\n')
                
    def inputFromJSON(self, filename):
        with open(filename, 'r', encoding='utf8') as filein:
            for line in filein:
                line = line.strip()
                query = json.loads(line)
                for obj in query:
                    self.path_list.append(Path(obj['Lat'], obj['Lng'], obj['RouteId'], obj['RouteVarId']))
            
