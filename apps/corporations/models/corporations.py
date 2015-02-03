from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Corporation(models.Model):
    """ corporations info """
    
    user = models.ForeignKey(User)
    api = models.OneToOneField("apies.Api")
    corporationID = models.IntegerField()
    corporationName = models.CharField(max_length=254)

    def __unicode__(self):
        return self.corporationName

    
    #connect to eveapi
    @staticmethod
    def static_auth():
        api = eveapi.EVEAPIConnection()
        auth = api.auth(keyID= setting.CORP_KEY, vCode=setting.CORP_VCODE)
        return auth

    
    #killboard
    @staticmethod
    def static_killLog():
        auth = Corporation.auth()
        return auth.corp.KillLog()
    
