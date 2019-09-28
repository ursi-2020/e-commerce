import sys

from django.http import HttpResponse
from apipkg import api_manager as api
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.http import JsonResponse
from .models import Produit
from . import models

import json

# Display index page, which is sign up page
def index(request):
   #time = api.send_request('scheduler', 'clock/time')
   #return HttpResponse("L'heure de la clock est %r" % time)
   return render(request, 'index.html')


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

# Load data to E-commerce DB from Catalogue DB
def displayProducts(request):
    products = api.send_request("catalogue-produit", "catalogueproduit/api/data")
    data = json.loads(products)
    for produit in data['produits']:
        p = Produit(codeProduit=produit['codeProduit'], familleProduit=produit['familleProduit'],
                        descriptionProduit=produit['descriptionProduit'], prix=produit['prix'], quantiteMin=1, packaging=0)
        p.save()
    product_list = {
        "data" : Produit.objects.all()
    }
    return render(request, "products.html", product_list)

# Clear DB
def removeDB(request):
    models.Produit.objects.all().delete()
    product_list = {
        "data" : Produit.objects.all()
    }
    return render(request, "products.html", product_list)