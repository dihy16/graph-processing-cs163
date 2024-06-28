import csv
import json

from RouteVar import *


class RouteVarQuery:
    def __init__(self, route_var_list):
        self.RouteVar_list = route_var_list
        
    def searchByRouteID(self, routeID):
        lst = [route_var for route_var in self.RouteVar_list if route_var.getRouteID() == routeID]
        return lst
    
    def searchByRouteVarID(self, routeVarID):
        lst = [route_var for route_var in self.RouteVar_list if route_var.getRouteVarID() == routeVarID]
        return lst
    
    def searchByRouteVarName(self, routeVarName):
        lst = [route_var for route_var in self.RouteVar_list if route_var.getRouteVarName() == routeVarName]
        return lst
    
    def searchByRouteShortName(self, routeVarShortName):
        lst = [route_var for route_var in self.RouteVar_list if route_var.getRouteShortName() == routeVarShortName]
        return lst
    
    def searchByStartStop(self, startStop):
        lst = [route_var for route_var in self.RouteVar_list if route_var.getStartStop() == startStop]
        return lst
    
    def searchByEndStop(self, endStop):
        lst = [route_var for route_var in self.RouteVar_list if route_var.getEndStop() == endStop]
        return lst
    
    def searchByDistance(self, distance):
        lst = [route_var for route_var in self.RouteVar_list if route_var.getDistance() == distance]
        return lst
    
    def searchByOutbound(self, outbound):
        lst = [route_var for route_var in self.RouteVar_list if route_var.getOutbound() == outbound]
        return lst
    
    def searchByRunningTime(self, runningTime):
        lst = [route_var for route_var in self.RouteVar_list if route_var.getRunningTime() == runningTime]
        return lst

    def outputAsCSV(query_list):
        with open('output.csv', 'w', newline='') as fileout:
            fieldnames = ['RouteID', 'RouteVarID', 'RouteVarName', 'RouteShortName', 'StartStop', 'EndStop', 'Distance', 'Outbound', 'RunningTime']
            csv_writer = csv.DictWriter(fileout, fieldnames=fieldnames)
            csv_writer.writeheader()
            for query in query_list:
                csv_writer.writerow(query)

    def outputAsJSON(query_list):
        with open('output.json', 'w') as fileout:
            for query in query_list:
                json.dump(query, fileout)
                fileout.write('\n')
