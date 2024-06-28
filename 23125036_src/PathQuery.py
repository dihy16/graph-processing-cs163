import csv
import json


class PathQuery:
    def __init__(self, path_list):
        self.path_list = path_list
        
    def searchByLat(self, lat):
        lst = [path for path in self.path_list if path.getLat() == lat]
        return lst
    
    def searchByLng(self, lng):
        lst = [path for path in self.path_list if path.getLng() == lng]
        return lst
    
    def searchByRouteID(self, routeID):
        lst = [path for path in self.path_list if path.getRouteID() == routeID]
        return lst
    
    def searchByRouteVarID(self, routeVarID):
        lst = [path for path in self.path_list if path.getRouteVarID() == routeVarID]
        return lst

    def outputAsCSV(query_list):
        with open('path_output.csv', 'w', newline='') as fileout:
            fieldnames = ['Lat', 'Lng', 'RouteID', 'RouteVarID']
            csv_writer = csv.DictWriter(fileout, fieldnames=fieldnames)
            csv_writer.writeheader()
            for query in query_list:
                csv_writer.writerow(query.__dict__)

    def outputAsJSON(query_list):
        with open('path_output.json', 'w') as fileout:
            for query in query_list:
                json.dump(query.__dict__, fileout)
                fileout.write('\n')
