from django.db import models

class Attribute(models.Model):
    """ all attributes """
    
    name = models.CharField(max_length=254, unique=True)
    
    def __unicode__(self):
        return self.name
    
