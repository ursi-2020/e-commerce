from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('hello', views.helloWolrd, name='hello'),
    #path('print', views.printJson, name='print'),
    #path('ihm', views.displayForm, name='field'),
    #path('search', views.search, name='search'),
    #path('save', views.saveDB, name='save'),
    path('read', views.readDB, name='read'),
    #path('info', views.getInfo, name='info'),
    path('products', views.displayProducts, name='products'),
    path('remove', views.removeDB, name='remove'),
    path('connect', views.connect, name="connect")
]