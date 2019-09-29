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

import json


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
    products = api.send_request("catalogue-produit", "api/data")
    data = json.loads(products)
    for produit in data['produits']:
        p = Produit(codeProduit=produit['codeProduit'], familleProduit=produit['familleProduit'],
                        descriptionProduit=produit['descriptionProduit'], prix=produit['prix'], quantiteMin=1, packaging=0)
        p.save()
    product_list = {
        "data" : Produit.objects.all()
    }
    return render(request, "products.html", product_list)


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
    print(username)
    print(password)
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

def displayScheduler(request):
    return render(request, "scheduler.html")

############################################################ END SCHEDULER ###########################################################