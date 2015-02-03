import eveapi
from apps.static.models import ConquerableStation



def add_stations():
    api = eveapi.EVEAPIConnection()
    
    outposts = api.eve.ConquerableStationList().outposts
    
    for o in outposts:
        try:
            ConquerableStation.objects.create(
                stationID = o.stationID,
                stationName = o.stationName,
                stationTypeID = o.stationTypeID,
                solarSystemID = o.solarSystemID,
                corporationID = o.corporationID,
                corporationName = o.corporationName,
            )
        except:
            print "aaapje faalhaas"
        

add_stations()




