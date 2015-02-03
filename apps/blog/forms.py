from datetime import datetime

from django import forms
from django.utils.text import slugify

from apps.blog.models import Article


class ArticleForm(forms.ModelForm):
    """ blog post form """
    
    class Meta:
        model = Article
        fields = ["title", "body", "public", "published"]
    
    
    def save_new(self, user, corp):
        title = self.cleaned_data['title']
        slug = slugify(title)
        try:
            Article.objects.get(slug=slug).exists()
            date = " %s" % datetime.now().strftime("%B %d, %Y %H:%M:%S")
            slug = slugify(slug + date)
        except Article.DoesNotExist:
            pass
        
        Article.objects.create(
            title = title,
            slug=slug,
            body = self.cleaned_data['body'],
            corp = corp,
            published = self.cleaned_data['published'],
            modified = datetime.now(),
            author = user,
        )
    
    
    #safe when object is modified
    def save(self, commit=True):
        form = super(ArticleForm, self).save(commit=False)
        title = self.cleaned_data['title']
        slug = slugify(title)
        try:
            Article.objects.filter(slug=slug).exists()
            slug = slugify(slug + " %s" % datetime.now().strftime("%B %d, %Y %H:%M:%S"))
        except Article.DoesNotExist:
            pass
            
        if commit:
            form.slug=slug
            form.save()
        return form
        
        
        
        
            
