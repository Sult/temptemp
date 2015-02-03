from django.db import models



class WalletRefTypes(models.Model):
    """ binds id to description """
    
    refTypeID = models.IntegerField(unique=True)
    refTypeName = models.CharField(max_length=254)
    
    def __unicode__(self):        
        return self.refTypeName
