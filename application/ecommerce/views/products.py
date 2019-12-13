import sys

from django.http import HttpResponse
from apipkg import api_manager as api
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.http import JsonResponse
from ..models import Produit
from ..models import Promotion
from ..models import ClientPromotion
from ..models import PromotionsCustomersProducts
from .. import models
from datetime import datetime, timedelta

import os, json
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
    all_client_promotions = ClientPromotion.objects.all()
    product_list = {
        "data" : all_producsts,
        "promos" : all_promotions,
        "clients_promos" : all_client_promotions,
        "products_promos" : PromotionsCustomersProducts.objects.all()
    }
    return render(request, "products.html", product_list)


# Call Catalogue produits to get content of its DB
# Returns products' view with content of E-commerce DB
def addProducts(request):
    models.Produit.objects.all().delete()
    models.Promotion.objects.all().delete()
    models.ClientPromotion.objects.all().delete()
    models.PromotionsCustomersProducts.objects.all().delete()
    products = api.send_request("catalogue-produit", "api/get-ecommerce")
    data = json.loads(products)
    for produit in data['produits']:
        p = Produit(codeProduit=produit['codeProduit'], familleProduit=produit['familleProduit'],
                        descriptionProduit=produit['descriptionProduit'], prix=produit['prix'], quantiteMin=1, packaging=0, exclusivite=produit['exclusivite'], id_catalogue=2)
        p.save()
    
    all_producsts = Produit.objects.all()
    for product in all_producsts:
        product.prix = product.prix / 100
    all_promotions = getPromotions()
    for promo in all_promotions:
        promo.prix = promo.prix / 100
        promo.prixOriginel = promo.prixOriginel / 100
    all_client_promotions = getClientPromotions()
    all_products_promotions = getProductPromotions()
    print("test 1 = " + str(all_client_promotions))
    product_list = {
        "data" : all_producsts,
        "promos" : all_promotions,
        "clients_promos" : all_client_promotions,
        "products_promos" : all_products_promotions
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
    models.ClientPromotion.objects.all().delete()
    models.PromotionsCustomersProducts.objects.all().delete()
    product_list = {
        "data" : Produit.objects.all(),
        "promos" : Promotion.objects.all(),
        "clients_promos" : ClientPromotion.objects.all(),
        "products_promos" : PromotionsCustomersProducts.objects.all()
    }
    return render(request, "products.html", product_list)

# Go to details page product
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


# Get promotions
def getPromotions():
    promotions = api.send_request("gestion-promotion", "promo/ecommerce")
    result = json.loads(promotions)
    result = result['promo']
    for promo in result:
        p2 = Promotion(codeProduit=promo['codeProduit'], familleProduit=promo['familleProduit'],
                        descriptionProduit=promo['descriptionProduit'], prix=promo['prix'], quantiteMin=promo['quantiteMin'], packaging=promo['packaging'], prixOriginel=promo['prixOriginel'], reduction=promo['reduction'])
        p2.save()
    return Promotion.objects.all()


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


# Returns pormotions for products
def getProductPromotions():
    promotions = api.send_request("gestion-promotion", "promo/customersproducts")
    
    result = json.loads(promotions)
    result = result['promo']
    for promo in result:
        p2 = PromotionsCustomersProducts(IdClient=promo['IdClient'], date=promo['date'],
                        reduction=promo['reduction'], codeProduit=promo['codeProduit'], quantity=promo['quantity'])
        p2.save()
    return PromotionsCustomersProducts.objects.all()


# Register functions
def register(request):
    r = requests.post('http://127.0.0.1:5001/register', data={'app': 'e-commerce',
                                                              'path': '/mnt/technical_base/e-commerce/application/ecommerce/static',
                                                              'route': 'http://127.0.0.1:9020/ecommerce/notifier'})
    return HttpResponse(r)

# Call this function when file is upload
@csrf_exempt
def receiveFileNotifier(request):
    print('ok je suis dans le notifier')
    r2 = requests.post('http://127.0.0.1:5001/manage')

    path_to_json = 'received_files/'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    for _file in json_files:
        models.Produit.objects.all().delete()
        print("received_files/" + _file)
        if (_file != "catalogue2.json"):
            json_data = open('received_files/' + _file)
            products = json.loads(json_data.read())
            for produit in products['produits']:
                p = Produit(codeProduit=produit['codeProduit'], familleProduit=produit['familleProduit'],
                        descriptionProduit=produit['descriptionProduit'], prix=produit['prix'], quantiteMin=1, packaging=0, exclusivite=produit['exclusivite'], id_catalogue=2)
                p.save()

    json_data.close()
    return HttpResponse("Done")