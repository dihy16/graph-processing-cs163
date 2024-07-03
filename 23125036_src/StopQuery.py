import csv
import json

from Stop import Stop

class StopQuery:
    def __init__(self, stop_list):
        self.stop_list = stop_list
        
    def searchByStopId(self, stopId):
        lst = [stop for stop in self.stop_list if stop.getStopId() == stopId]
        return lst
    
    def searchByCode(self, code):
        lst = [stop for stop in self.stop_list if stop.getCode() == code]
        return lst
    
    def searchByName(self, name):
        lst = [stop for stop in self.stop_list if stop.getName() == name]
        return lst
    
    def searchByStopType(self, stopType):
        lst = [stop for stop in self.stop_list if stop.getStopType() == stopType]
        return lst
    
    def searchByZone(self, zone):
        lst = [stop for stop in self.stop_list if stop.getZone() == zone]
        return lst
    
    def searchByWard(self, ward):
        lst = [stop for stop in self.stop_list if stop.getWard() == ward]
        return lst
    
    def searchByAddressNo(self, addressNo):
        lst = [stop for stop in self.stop_list if stop.getAddressNo() == addressNo]
        return lst
    
    def searchByStreet(self, street):
        lst = [stop for stop in self.stop_list if stop.getStreet() == street]
        return lst
    
    def searchBySupportDisability(self, supportDisability):
        lst = [stop for stop in self.stop_list if stop.getSupportDisability() == supportDisability]
        return lst
    
    def searchByStatus(self, status):
        lst = [stop for stop in self.stop_list if stop.getStatus() == status]
        return lst
    
    def searchByLng(self, lng):
        lst = [stop for stop in self.stop_list if stop.getLng() == lng]
        return lst
    
    def searchByLat(self, lat):
        lst = [stop for stop in self.stop_list if stop.getLat() == lat]
        return lst
    
    def searchBySearch(self, search):
        lst = [stop for stop in self.stop_list if stop.getSearch() == search]
        return lst
    
    def searchByRoutes(self, route):
        lst = [stop for stop in self.stop_list if route in stop.getRoutes()]
        return lst
    
    def searchByRouteId(self, routeId):
        lst = [stop for stop in self.stop_list if stop.getRouteId() == routeId]
        return lst
    
    def searchByRouteVarId(self, routeVarId):
        lst = [stop for stop in self.stop_list if stop.getRouteVarId() == routeVarId]
        return lst

    def outputAsCSV(self, query_list, filename):
        with open(filename, 'w', encoding='utf8', newline='') as fileout:
            fieldnames = ['StopId', 
                          'Code', 
                          'Name', 
                          'StopType', 
                          'Zone', 
                          'Ward', 
                          'AddressNo', 
                          'Street', 
                          'SupportDisability', 
                          'Status', 
                          'Lng', 
                          'Lat', 
                          'Search', 
                          'Routes',
                          'RouteId',
                          'RouteVarId'
                          ]
            csv_writer = csv.DictWriter(fileout, fieldnames=fieldnames)
            csv_writer.writeheader()
            for query in query_list:
                csv_writer.writerow(query.__dict__)

    def outputAsJSON(self, query_list, filename):
        with open(filename, 'w', encoding='utf8') as fileout:
            for query in query_list:
                queryDict = query.__dict__
                queryDict['Routes'] =','.join(query.getRoutes())
                json.dump(queryDict, fileout, ensure_ascii=False)
                fileout.write('\n')
                
    def inputFromJSON(self, filename):
        with open(filename, 'r', encoding='utf8') as filein:
            for line in filein:
                query = json.loads(line)
                for stop in query['Stops']:
                    self.stop_list.append(Stop(stop['StopId'], 
                                              stop['Code'], 
                                              stop['Name'], 
                                              stop['StopType'], 
                                              stop['Zone'], 
                                              stop['Ward'], 
                                              stop['AddressNo'], 
                                              stop['Street'], 
                                              stop['SupportDisability'], 
                                              stop['Status'], 
                                              stop['Lng'], 
                                              stop['Lat'], 
                                              stop['Search'], 
                                              stop['Routes'].split(','),
                                              query['RouteId'], 
                                              query['RouteVarId']
                                              )
                                        )
