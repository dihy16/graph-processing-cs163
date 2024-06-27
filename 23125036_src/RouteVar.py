class RouteVar:
    def __init__(self, RouteID, RouteVarID, RouteVarName, RouteVarShortName, RouteNo, StartStop, EndStop, Distance, Outbound, RunningTime):
        self.RouteID = RouteID
        self.RouteVarID = RouteVarID
        self.RouteVarName = RouteVarName
        self.RouteVarShortName = RouteVarShortName
        self.RouteNo = RouteNo
        self.StartStop = StartStop
        self.EndStop = EndStop
        self.Distance = Distance
        self.Outbound = Outbound
        self.RunningTime = RunningTime
       
    def getRouteID(self):
        return self.RouteID
    def setRouteID(self, x):
        self.RouteID = x
        
    def getRouteVarID(self):
        return self.RouteVarID
    def setRouteVarID(self, x):
        self.RouteVarID = x
        
    def getRouteVarName(self):
        return self.RouteVarName
    def setRouteVarName(self, x):
        self.RouteVarName = x
        
    def getRouteVarShortName(self):
        return self.RouteVarShortName
    def setRouteVarShortName(self, x):
        self.RouteVarShortName = x
        
    def getRouteNo(self):
        return self.RouteNo
    def setRouteNo(self, x):
        self.RouteNo = x
        
    def getStartStop(self):
        return self.StartStop
    def setStartStop(self, x):
        self.StartStop = x
        
    def getEndStop(self):
        return self.EndStop
    def setEndStop(self, x):
        self.EndStop = x
        
    def getDistance(self):
        return self.Distance
    def setDistance(self, x):
        self.Distance = x
        
    def getOutbound(self):
        return self.Outbound
    def setOutbound(self, x):
        self.Outbound = x

    def getRunningTime(self):
        return self.RunningTime
    def setRunningTime(self, x):
        self.RunningTime = x


