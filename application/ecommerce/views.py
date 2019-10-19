import sys

from django.http import HttpResponse
from apipkg import api_manager as api
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.http import JsonResponse
from .models import Produit
from .models import Customer
from . import models
from datetime import datetime, timedelta

import json
import requests


# Display index page
# Return the signup (index.html) view
def index(request):
   #time = api.send_request('scheduler', 'clock/time')
   #return HttpResponse("L'heure de la clock est %r" % time)
   return render(request, 'index.html')


############################################################## PRODUCTS ##############################################################


# Display products from E-commerce DB
# Returns the products' view
def displayProducts(request):
    product_list = {
        "data" : Produit.objects.all()
    }
    return render(request, "products.html", product_list)


# Call Catalogue produits to get content of its DB
# Returns products' view with content of E-commerce DB
def addProducts(request):
    products = api.send_request("catalogue-produit", "api/get-ecommerce")
    data = json.loads(products)
    for produit in data['produits']:
        p = Produit(codeProduit=produit['codeProduit'], familleProduit=produit['familleProduit'],
                        descriptionProduit=produit['descriptionProduit'], prix=produit['prix'], quantiteMin=1, packaging=0)
        p.save()
    product_list = {
        "data" : Produit.objects.all()
    }
    return render(request, "products.html", product_list)


# Call Catalogue produits to get content of its DB automatically
@csrf_exempt
def addProductsAuto(request):
    print("Added automatically products")
    products = api.send_request("catalogue-produit", "api/get-ecommerce")
    data = json.loads(products)
    for produit in data['produits']:
        p = Produit(codeProduit=produit['codeProduit'], familleProduit=produit['familleProduit'],
                        descriptionProduit=produit['descriptionProduit'], prix=produit['prix'], quantiteMin=1, packaging=0)
        p.save()
    return HttpResponse("Done")


# Remove all products from DB
# Returns the products' view
def removeDB(request):
    models.Produit.objects.all().delete()
    product_list = {
        "data" : Produit.objects.all()
    }
    return render(request, "products.html", product_list)


############################################################ END PRODUCTS ############################################################



############################################################## CUSTOMERS #############################################################


# Add user to CRM and then connect
# Returns products' view with current products in E-commerce DB
def connect(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    body = {
        'firstName' : username,
        'lastName' : password
    }
    body = json.dumps(body)
    # signup = api.post_request("crm", "/api/update_db", body)
    product_list = {
        "data" : Produit.objects.all()
    }
    return render(request, 'products.html', product_list)


# Display all clients from DB
# Returns customers' view with current customers in E-commerce DB
def displayCustomers(request):
    customer_list = {
        "data" : Customer.objects.all()
    }
    return render(request, "customers.html", customer_list)

# Load customers from CRM
# Returns customer's view
def loadCustomers(request):
    customers = api.send_request("crm", "api/data")
    data = json.loads(customers)
    for customer in data:
        customer_tmp = Customer(firstName=customer['firstName'], lastName=customer['lastName'],
                        fidelityPoint=customer['fidelityPoint'], payment=customer['payment'], account=customer["account"])
        customer_tmp.save()
    customers_list = {
        "data" : Customer.objects.all()
    }
    return render(request, "customers.html", customers_list)


# Function use for scheduler
# Post function to get customers from CRM
@csrf_exempt
def loadCustomersAuto(request):
    customers = api.send_request("crm", "api/data")
    data = json.loads(customers)
    for customer in data:
        customer_tmp = Customer(firstName=customer['firstName'], lastName=customer['lastName'],
                        fidelityPoint=customer['fidelityPoint'], payment=customer['payment'], account=customer["account"])
        customer_tmp.save()
    return HttpResponse("Done")


# Remove all Customers in E-commerce DB
# Returns the customers' view
def removeCustomers(request):
    models.Customer.objects.all().delete()
    customers_list = {
        "data" : Customer.objects.all()
    }
    return render(request, "customers.html", customers_list)


############################################################ END CUSTOMERS ###########################################################




############################################################## SCHEDULER #############################################################

# Display scheduler page
# Get info and scheduled tasks list
def displayScheduler(request):
    info = api.send_request("scheduler", "clock/info")
    tasks = api.send_request("scheduler", "schedule/list")
    info = json.loads(info)
    info = {
        "data" : info,
        "tasks" : tasks
    }
    return render(request, "scheduler.html", info)


# Add a task to scheduler using the form
def addTaskScheduler(request):
    data = request.POST.dict()
    time = datetime.strptime(data["time"], '%Y-%m-%dT%H:%M')
    host = ""
    recurrence = data["recurrence"]
    url = ""
    source = "e-commerce"
    name = "get_customers"
    data2 = ""
    if data["app"] == "products":
        host = "e-commerce"
        url = "ecommerce/add-auto"
        name = "get_products"
    elif data["app"] == "crm":
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
    return render(request, "scheduler.html", info)


# Function used to schedule a task
def schedule_task(host, url, time, recurrence, data, source, name):
    time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
    headers = {'Host': 'scheduler'}
    data = {"target_url": url, "target_app": host, "time": time_str, "recurrence": recurrence, "data": data, "source_app": source, "name": name}
    r = requests.post(api.api_services_url + 'schedule/add', headers = headers, json = data)
    print(r.status_code)
    print(r.text)
    return r.text


# Remove all tasks from scheduler
@csrf_exempt
def removeAllTasks(request):
    remove = api.post_request("scheduler", "app/delete?source=ecommerce", '{source: "ecommerce"}')
    print(remove)
    return HttpResponse("done")

############################################################ END SCHEDULER ###########################################################