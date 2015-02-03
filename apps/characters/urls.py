from django.conf.urls import patterns, url

from apps.characters import views

urlpatterns = patterns('',
    url(r'^characters/$', views.characters, name='characters'),
    url(r'^characters/(?P<pk>\d+)/$', views.select_character, name='select_character'),

    #character pages
    url(r'^character/$', views.character_sheet, name='character_sheet'),
    url(r'^character/skills/$', views.character_skills, name='character_skills'),
    url(r'^character/wallet/journal/$', views.wallet_journal, name='wallet_journal'),
    url(r'^character/market/transactions/$', views.market_transactions, name='market_transactions'),
    #url(r'^character/market/orders/$', views.market_orders, name='market_orders'),
    url(r'^character/killboard/$', views.character_killboard, name='character_killboard'),
)
