from django.conf.urls import patterns, url

from apps.apies import views

urlpatterns = patterns('',
    url(r'^apies/$', views.apies, name='apies'),
    url(r'^apies/update/(?P<pk>\d+)/$', views.update_api, name='update_api'),
    url(r'^apies/delete/(?P<pk>\d+)/$', views.delete_api, name='delete_api'),
)

