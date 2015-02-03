from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField


class Article(models.Model):
    """Represents a blog article"""
    
    title = models.CharField(max_length=62, blank=True)
    slug = models.SlugField(unique=True, max_length=100)
    body = FroalaField()
    
    public = models.BooleanField(default=True)
    published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    corp = models.BooleanField(default=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User)

    
    def __unicode(self):
        return self.title
    
    
    def show_modified(self):
        return self.modified.strftime("%B %d, %Y %H:%M")
    
