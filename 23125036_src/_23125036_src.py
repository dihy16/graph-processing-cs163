from RouteVarQuery import RouteVarQuery

route_var_query = RouteVarQuery([])
route_var_query.inputFromJSON('data/vars.json')
route_var_query.outputAsJSON(route_var_query.searchByRouteId(35), 'data/route_var_output.json')
route_var_query.outputAsCSV(route_var_query.searchByStartStop('Bến xe buýt Kho Muối'), 'data/route_var_output.csv')

