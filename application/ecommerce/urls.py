from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products', views.displayProducts, name='products'),
    path('remove', views.removeDB, name='remove'),
    path('connect', views.connect, name="connect")
]