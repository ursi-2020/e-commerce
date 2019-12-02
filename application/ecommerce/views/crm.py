import sys

from django.http import HttpResponse
from apipkg import api_manager as api
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from ..models import Customer
from ..models import Produit
from ..models import Promotion
from ..models import ClientPromotion
from .. import models
from datetime import datetime, timedelta

import json
import requests

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
    signup = api.post_request("crm", "/api/update_db", body)
    all_producsts = Produit.objects.all()
    for product in all_producsts:
        product.prix = product.prix / 100
    all_promotions = Promotion.objects.all()
    all_client_promotions = ClientPromotion.objects.all()
    for promo in all_promotions:
        promo.prix = promo.prix / 100
        promo.prixOriginel = promo.prixOriginel / 100
    product_list = {
        "data" : all_producsts,
        "promos" : all_promotions,
        "clients_promos" : all_client_promotions
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
        customer_tmp = Customer(IdClient=customer['IdClient'], Prenom=customer['Prenom'],
                        Nom=customer['Nom'], Credit=customer['Credit'], Paiement=customer["Paiement"], Compte=customer["Compte"], carteFid=customer["carteFid"])
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
        customer_tmp = Customer(IdClient=customer['IdClient'], Prenom=customer['Prenom'],
                        Nom=customer['Nom'], Credit=customer['Credit'], Paiement=customer["Paiement"], Compte=customer["Compte"], carteFid=customer["carteFid"])
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

# Get promotions
def getClientPromotions():
    promotions = api.send_request("gestion-promotion", "promo/customers")
    result = json.loads(promotions)
    result = result['promo']
    for promo in result:
        p2 = ClientPromotion(IdClient=promo['IdClient'], date=promo['date'],
                        reduction=promo['reduction'])
        p2.save()
    return ClientPromotion.objects.all()