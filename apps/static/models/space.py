from django.db import models

class ConquerableStation(models.Model):
    """ player outposts (nullsec stations) """
    
    stationID = models.IntegerField()
    stationName = models.CharField(max_length=254)
    stationTypeID = models.IntegerField()
    solarSystemID = models.IntegerField()
    corporationID = models.IntegerField()
    corporationName = models.CharField(max_length=254)
    
    def __unicode__(self):
        return self.stationName





