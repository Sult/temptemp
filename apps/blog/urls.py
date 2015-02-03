from django.conf.urls import patterns, url

from apps.blog import views

urlpatterns = patterns('',
    url(r'^blog/$', views.blog, name='blog'),
    url(r'^blog/admin/$', views.blog_admin, name='blog_admin'),
    url(r'^blog/admin/create/$', views.blog_create, name='blog_create'),
    url(r'^blog/admin/edit/(?P<slug>[\w-]+)/$', views.blog_edit, name='blog_edit'),
    url(r'^blog/admin/delete/(?P<pk>\d+)/$', views.blog_delete, name='blog_delete'),
)

