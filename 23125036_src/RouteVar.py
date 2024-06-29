class RouteVar:
    def __init__(self, RouteId, RouteVarId, RouteVarName, RouteVarShortName, RouteNo, StartStop, EndStop, Distance, Outbound, RunningTime):
        self.RouteId = RouteId
        self.RouteVarId = RouteVarId
        self.RouteVarName = RouteVarName
        self.RouteVarShortName = RouteVarShortName
        self.RouteNo = RouteNo
        self.StartStop = StartStop
        self.EndStop = EndStop
        self.Distance = Distance
        self.Outbound = Outbound
        self.RunningTime = RunningTime
       
    def getRouteId(self):
        return self.RouteId
    
    def setRouteId(self, x):
        self.RouteId = x
        
    def getRouteVarId(self):
        return self.RouteVarId
    
    def setRouteVarId(self, x):
        self.RouteVarId = x
        
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

