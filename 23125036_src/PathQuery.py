import csv
import json

from Path import Path

class PathQuery:
    def __init__(self, path_list):
        self.path_list = path_list
        
    def searchByLat(self, lat_parameter):
        lst = []
        for path in self.path_list:
            lat_list = path.getLatList()
            for lat in lat_list:
                if lat == lat_parameter:
                    lst.append(path)
        return lst
    
    def searchByLng(self, lng_parameter):
        lst = []
        for path in self.path_list:
            lng_list = path.getLngList()
            for lng in lng_list:
                if lng == lng_parameter:
                    lst.append(path)
        return lst
    
    def searchByRouteId(self, routeId):
        lst = [path for path in self.path_list if path.getRouteId() == routeId]
        return lst
    
    def searchByRouteVarId(self, routeVarId):
        lst = [path for path in self.path_list if path.getRouteVarId() == routeVarId]
        return lst

    def outputAsCSV(self, query_list, filename):
        with open(filename, 'w', encoding='utf8', newline='') as fileout:
            fieldnames = ['lat', 'lng', 'RouteId', 'RouteVarId']
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
                query = json.loads(line)
                self.path_list.append(Path(query['lat'], query['lng'], query['RouteId'], query['RouteVarId']))
            
