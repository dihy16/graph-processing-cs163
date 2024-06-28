import csv
import json


class StopQuery:
    def __init__(self, stop_list):
        self.stop_list = stop_list
        
    def searchByStopID(self, stopID):
        lst = [stop for stop in self.stop_list if stop.getStopID() == stopID]
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
    
    def searchByRoutes(self, routes):
        lst = [stop for stop in self.stop_list if stop.getRoutes() == routes]
        return lst

    def outputAsCSV(query_list):
        with open('stop_output.csv', 'w', newline='') as fileout:
            fieldnames = ['StopID', 'Code', 'Name', 'StopType', 'Zone', 'Ward', 'AddressNo', 'Street', 'SupportDisability', 'Status', 'Lng', 'Lat', 'Search', 'Routes']
            csv_writer = csv.DictWriter(fileout, fieldnames=fieldnames)
            csv_writer.writeheader()
            for query in query_list:
                csv_writer.writerow(query.__dict__)

    def outputAsJSON(query_list):
        with open('stop_output.json', 'w') as fileout:
            for query in query_list:
                json.dump(query.__dict__, fileout)
                fileout.write('\n')
