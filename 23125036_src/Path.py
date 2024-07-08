class Path:
    def __init__(self, Lat, Lng, RouteId, RouteVarId):
        self.Lat = Lat
        self.Lng = Lng
        self.RouteId = RouteId
        self.RouteVarId = RouteVarId

    def getLatList(self):
        return self.Lat

    def setLatList(self, Lat):
        self.Lat = Lat

    def getLngList(self):
        return self.Lng

    def setLngList(self, Lng):
        self.Lng = Lng

    def getRouteId(self):
        return self.RouteId

    def setRouteId(self, RouteId):
        self.RouteId = RouteId

    def getRouteVarId(self):
        return self.RouteVarId

    def setRouteVarId(self, RouteVarId):
        self.RouteVarId = RouteVarId
