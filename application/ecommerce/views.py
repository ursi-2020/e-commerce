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

# Display index page, which is sign up page
def index(request):
   #time = api.send_request('scheduler', 'clock/time')
   #return HttpResponse("L'heure de la clock est %r" % time)
   return render(request, 'index.html')


############################################################## PRODUCTS ##############################################################

# Display products from E-commerce DB
def displayProducts(request):
    product_list = {
        "data" : Produit.objects.all()
    }
    return render(request, "products.html", product_list)


# Load products from Catalogue DB
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
def removeDB(request):
    models.Produit.objects.all().delete()
    product_list = {
        "data" : Produit.objects.all()
    }
    return render(request, "products.html", product_list)

############################################################ END PRODUCTS ############################################################



############################################################## CUSTOMERS #############################################################

# Add user to CRM and then connect
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
def displayCustomers(request):
    customer_list = {
        "data" : Customer.objects.all()
    }
    return render(request, "customers.html", customer_list)

# Load cistomers from CRM
def loadCustomers(request):
    customers = api.send_request("crm", "/data")
    data = json.loads(products)

############################################################ END CUSTOMERS ###########################################################




############################################################## SCHEDULER #############################################################

def displayScheduler(request):
    return render(request, "scheduler.html")

############################################################ END SCHEDULER ###########################################################