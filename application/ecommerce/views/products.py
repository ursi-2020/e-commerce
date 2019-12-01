import sys

from django.http import HttpResponse
from apipkg import api_manager as api
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.http import JsonResponse
from ..models import Produit
from ..models import Promotion
from .. import models
from datetime import datetime, timedelta

import json
import requests


# Display products from E-commerce DB
# Returns the products' view
def displayProducts(request):
    all_producsts = Produit.objects.all()
    for product in all_producsts:
        product.prix = product.prix / 100
    all_promotions = Promotion.objects.all()
    for promo in all_promotions:
        promo.prix = promo.prix / 100
        promo.prixOriginel = promo.prixOriginel / 100
    product_list = {
        "data" : all_producsts,
        "promos" : all_promotions
    }
    return render(request, "products.html", product_list)


# Call Catalogue produits to get content of its DB
# Returns products' view with content of E-commerce DB
def addProducts(request):
    products = api.send_request("catalogue-produit", "api/get-ecommerce")
    data = json.loads(products)
    for produit in data['produits']:
        p = Produit(codeProduit=produit['codeProduit'], familleProduit=produit['familleProduit'],
                        descriptionProduit=produit['descriptionProduit'], prix=produit['prix'], quantiteMin=1, packaging=0, exclusivite=produit['exclusivite'], id_catalogue=produit['id'])
        p.save()
    promotions = api.send_request("gestion-promotion", "promo/ecommerce")
    data2 = json.loads(promotions)
    data2 = json.loads(data2)
    for promo in data2:
        p2 = Promotion(codeProduit=promo['fields']['codeProduit'], familleProduit=promo['fields']['familleProduit'],
                        descriptionProduit=promo['fields']['descriptionProduit'], prix=promo['fields']['prix'], quantiteMin=promo['fields']['quantiteMin'], packaging=promo['fields']['packaging'], prixOriginel=promo['fields']['prixOriginel'], reduction=promo['fields']['reduction'])
        p2.save()


    all_producsts = Produit.objects.all()
    for product in all_producsts:
        product.prix = product.prix / 100
    all_promotions = Promotion.objects.all()
    for promo in all_promotions:
        promo.prix = promo.prix / 100
        promo.prixOriginel = promo.prixOriginel / 100
    product_list = {
        "data" : all_producsts,
        "promos" : all_promotions
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
                        descriptionProduit=produit['descriptionProduit'], prix=produit['prix'], quantiteMin=1, packaging=0, exclusivite=produit['exclusivite'], id_catalogue=produit['id'])
        p.save()

    
    promotions = api.send_request("gestion-promotion", "promo/ecommerce")
    data2 = json.loads(promotions)
    data2 = json.loads(data2)
    for promo in data2:
        p2 = Promotion(codeProduit=promo['fields']['codeProduit'], familleProduit=promo['fields']['familleProduit'],
                        descriptionProduit=promo['fields']['descriptionProduit'], prix=promo['fields']['prix'], quantiteMin=promo['fields']['quantiteMin'], packaging=promo['fields']['packaging'], prixOriginel=promo['fields']['prixOriginel'], reduction=promo['fields']['reduction'])
        p2.save()

    return HttpResponse("Done")


# Remove all products from DB
# Returns the products' view
def removeDB(request):
    models.Produit.objects.all().delete()
    models.Promotion.objects.all().delete()
    product_list = {
        "data" : Produit.objects.all(),
        "promos" : Promotion.objects.all()
    }
    return render(request, "products.html", product_list)

def goToProduct(request, pk):
    product = api.send_request("catalogue-produit", "api/get-by-id/" + str(pk))
    result = json.loads(product)
    result = result['produit']
    produit = Produit(codeProduit=result['codeProduit'], familleProduit=result['familleProduit'],
                        descriptionProduit=result['descriptionProduit'], prix=result['prix'], quantiteMin=1, packaging=0, id_catalogue=result['id'])
    data = {
        "product": produit
    }
    return render(request, "product.html", data)