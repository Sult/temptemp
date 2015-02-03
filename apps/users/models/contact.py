from django.db import models


class ContactMail(models.Model):
    """ get acces to contactmails made from site """
    
    title = models.CharField(max_length=254)
    email = models.EmailField(max_length=254)
    body = models.TextField()
    
    def __unicode__(self):
        return self.title
    
    
