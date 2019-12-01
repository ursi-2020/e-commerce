from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('products', views.displayProducts, name='products'),
    path('remove', views.removeDB, name='remove'),
    path('connect', views.connect, name="connect"),
    path('add', views.addProducts, name="add"),
    path('add-auto', views.addProductsAuto, name="add-auto"),
    path('product/<int:pk>', views.goToProduct, name="go-product"),

    path('customers', views.displayCustomers, name="customers"),
    path('load_customers', views.loadCustomers, name="load_customers"),
    path('auto_load_customers', views.loadCustomersAuto, name="auto_load_customers"),
    path('remove_customers', views.removeCustomers, name="remove_customers"),

    path('scheduler', views.displayScheduler, name="scheduler"),
    path('add_task', views.addTaskScheduler, name="add_task"),
    path('remove_tasks', views.removeAllTasks, name="remove_tasks"),


    path('create_customer', views.createCustomer, name="create-customer"),
    path('generate_ecomm_tickets', views.salesSimulation, name="sales-simulation"),


    path('getTickets', views.getTickets, name="get_tickets")
]