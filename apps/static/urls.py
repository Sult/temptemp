from django.conf.urls import patterns, url

from apps.static import views

urlpatterns = patterns('',
    url(r'^library/skilltree/$', views.tree, name='tree'),
    url(r'^library/skilltree/(?P<pk>\d+)/$', views.skilltree, name='skilltree'),
)

