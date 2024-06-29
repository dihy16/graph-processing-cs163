import csv
import json

from RouteVar import RouteVar

class RouteVarQuery:
    def __init__(self, route_var_list):
        self.RouteVar_list = route_var_list
        
    def searchByRouteId(self, routeId):
        lst = [route_var for route_var in self.RouteVar_list if route_var.getRouteId() == routeId]
        return lst
    
    def searchByRouteVarId(self, routeVarId):
        lst = [route_var for route_var in self.RouteVar_list if route_var.getRouteVarId() == routeVarId]
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

    def outputAsCSV(self, query_list, filename):
        with open(filename, 'w', encoding='utf8', newline='') as fileout:
            fieldnames = ['RouteId', 
                          'RouteVarId', 
                          'RouteVarName', 
                          'RouteVarShortName', 
                          'RouteNo',
                          'StartStop', 
                          'EndStop', 
                          'Distance', 
                          'Outbound', 
                          'RunningTime'
                          ]
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
                    self.RouteVar_list.append(RouteVar(obj['RouteId'], 
                                                   obj['RouteVarId'], 
                                                   obj['RouteVarName'], 
                                                   obj['RouteVarShortName'], 
                                                   obj['RouteNo'], 
                                                   obj['StartStop'], 
                                                   obj['EndStop'], 
                                                   obj['Distance'], 
                                                   obj['Outbound'], 
                                                   obj['RunningTime']
                                                   )
                                         )         
