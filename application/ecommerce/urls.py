from django.urls import path
from apipkg import api_manager as api
from datetime import datetime, timedelta
import json
import requests
from django.http import JsonResponse

from . import views

urlpatterns = [
    path('', views.index, name='index'),
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
    path('sales_simulation', views.salesSimulation, name="sales-simulation"),

    path('notifier', views.receiveFileNotifier, name="notifier"),

    path('sales', views.salesSimulation, name="sales"),

    path('getTickets', views.getTickets, name="get_tickets")
]


# Add a task to scheduler using the form
def addTaskScheduler():
    today = api.send_request('scheduler', 'clock/time')
    time = datetime.strptime(today, '"%d/%m/%Y-%H:%M:%S"')

    host = ""
    recurrence = "day"
    url = ""
    source = "e-commerce"
    name = "get_customers"
    data2 = ""
    # if data["app"] == "products":
    #     host = "e-commerce"
    #     url = "ecommerce/add-auto"
    #     name = "get_products"
    # elif data["app"] == "crm":
    host = "e-commerce"
    url = "ecommerce/auto_load_customers"
    name = "get_customers"
    schedule_task(host, url, time, recurrence, data2, source, name)

    info = api.send_request("scheduler", "clock/info")
    tasks = api.send_request("scheduler", "schedule/list")
    info = json.loads(info)
    info = {
        "data" : info,
        "tasks" : tasks
    }
    return JsonResponse({"State": "finished"})

# Function used to schedule a task
def schedule_task(host, url, time, recurrence, data, source, name):
    time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
    headers = {'Host': 'scheduler'}
    data = {"target_url": url, "target_app": host, "time": time_str, "recurrence": recurrence, "data": data, "source_app": source, "name": name}
    r = requests.post(api.api_services_url + 'schedule/add', headers = headers, json = data)
    return r.text

addTaskScheduler()