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

    def outputAsCSV(list):
        with open('output.csv', 'w', newline = '') as csvfile:
            fileout = csv.writer(csvfile)
            fileout.writerow(['RouteID', 'RouteVarID', 'RouteVarName', 'RouteShortName', 'StartStop', 'EndStop', 'Distance', 'Outbound', 'RunningTime'])
            for query in list:
                fileout.writerow([query.RouteID, query.RouteVarID, query.RouteVarName, query.RouteShortName, query.StartStop, query.EndStop, query.Distance, query.Outbound, query.RunningTime])

    def outputAsJSON(list):
        for query in list:
            json_object = json.dumps(query)
            with open('output.json', 'w') as fileout:
                fileout.write(json_object)
