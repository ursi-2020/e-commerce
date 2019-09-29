from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products', views.displayProducts, name='products'),
    path('remove', views.removeDB, name='remove'),
    path('connect', views.connect, name="connect"),
    path('add', views.addProducts, name="add"),

    path('customers', views.displayCustomers, name="customers"),
    path('load_customers', views.loadCustomers, name="load_customers"),
    path('remove_customers', views.removeCustomers, name="remove_customers"),

    path('scheduler', views.displayScheduler, name="scheduler")    
]