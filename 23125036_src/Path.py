class Path:
    def __init__(self, Lat, Lng, RouteID, RouteVarID):
        self.Lat = Lat
        self.Lng = Lng
        self.RouteID = RouteID
        self.RouteVarID = RouteVarID

    def getLat(self):
        return self.Lat

    def setLat(self, Lat):
        self.Lat = Lat

    def getLng(self):
        return self.Lng

    def setLng(self, Lng):
        self.Lng = Lng

    def getRouteID(self):
        return self.RouteID

    def setRouteID(self, RouteID):
        self.RouteID = RouteID

    def getRouteVarID(self):
        return self.RouteVarID

    def setRouteVarID(self, RouteVarID):
        self.RouteVarID = RouteVarID
