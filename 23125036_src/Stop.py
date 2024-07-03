class Stop:
    def __init__(self, StopId, Code, Name, StopType, Zone, Ward, AddressNo, Street, SupportDisability, Status, Lng, Lat, Search, Routes, RouteId, RouteVarId):
        self.StopId = StopId
        self.Code = Code
        self.Name = Name
        self.StopType = StopType
        self.Zone = Zone
        self.Ward = Ward
        self.AddressNo = AddressNo
        self.Street = Street
        self.SupportDisability = SupportDisability
        self.Status = Status
        self.Lng = Lng
        self.Lat = Lat
        self.Search = Search
        self.Routes = Routes
        self.RouteId = RouteId
        self.RouteVarId = RouteVarId
        
    def getStopId(self):
        return self.StopId

    def setStopId(self, StopId):
        self.StopId = StopId

    def getCode(self):
        return self.Code

    def setCode(self, Code):
        self.Code = Code

    def getName(self):
        return self.Name

    def setName(self, Name):
        self.Name = Name

    def getStopType(self):
        return self.StopType

    def setStopType(self, StopType):
        self.StopType = StopType

    def getZone(self):
        return self.Zone

    def setZone(self, Zone):
        self.Zone = Zone
        
    def getWard(self):
        return self.Ward

    def setWard(self, Ward):
        self.Ward = Ward

    def getAddressNo(self):
        return self.AddressNo

    def setAddressNo(self, AddressNo):
        self.AddressNo = AddressNo

    def getStreet(self):
        return self.Street

    def setStreet(self, Street):
        self.Street = Street

    def getSupportDisability(self):
        return self.SupportDisability

    def setSupportDisability(self, SupportDisability):
        self.SupportDisability = SupportDisability

    def getStatus(self):
        return self.Status

    def setStatus(self, Status):
        self.Status = Status

    def getLng(self):
        return self.Lng

    def setLng(self, Lng):
        self.Lng = Lng

    def getLat(self):
        return self.Lat

    def setLat(self, Lat):
        self.Lat = Lat

    def getSearch(self):
        return self.Search

    def setSearch(self, Search):
        self.Search = Search

    def getRoutes(self):
        return self.Routes

    def setRoutes(self, Routes):
        self.Routes = Routes

    def getRouteId(self):
        return self.RouteId

    def setRouteId(self, routeId):
        self.RouteId = routeId

    def getRouteVarId(self):
        return self.RouteVarId

    def setRouteId(self, routeVarId):
        self.RouteVarId = routeVarId