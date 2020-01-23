import sys

from django.http import HttpResponse
from apipkg import api_manager as api
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.http import JsonResponse
from ..models import Produit
from ..models import Customer
from ..models import Promotion
from ..models import ClientPromotion
from ..models import PromotionsCustomersProducts
from ..models import Tickets
from .. import models
from datetime import datetime, timedelta
from django.core import serializers



import json
import requests


@csrf_exempt
def createCustomer(request):
    body_unicode = request.body.decode('latin-1')
    body = json.loads(body_unicode)
    nom = body["Nom"]
    
    if "Compte" in body :
        generated_body = {
            "Nom" : nom,
            "Prenom" : body["Prenom"],
            "email" : body["email"],
            "Credit" : body["Credit"],
            "Paiement" : body["Paiement"],
            "Compte" : body["Compte"]
        }
    else :
        generated_body = {
            "Nom" : nom,
            "Prenom" : body["Prenom"],
            "email" : body["email"],
            "Credit" : (body["Credit"]),
            "Paiement" : body["Paiement"],
            "Compte" : ""
        }
    
    generated_body = json.dumps(generated_body)
    generated_body = json.loads(generated_body)
    status, response = api.post_request2("crm", "/api/create_customer", json.dumps(generated_body))

    response = json.loads(response.text)
    id = response["idClient"]

    return JsonResponse({
        "CarteFid" : id
    })

@csrf_exempt
def salesSimulation(request):
    body_unicode = request.body.decode('latin-1')
    body = json.loads(body_unicode)

    testSales(body)
    return HttpResponse("done")


def testSales(data):
    return_tickets = []

    all_articles_calculated = []

    data = json.dumps(data)
    data = json.loads(data)

    # Tickets array
    ticket = data

    # Retrieve products
    products = Produit.objects.all()

    clock_time = api.send_request('scheduler', 'clock/time')
    time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    date = time

    # Variable declaration
    new_sale = {
        "id" : 0,
        "date" : date,
        "prix" : 0,
        "client" : "",
        "pointsFidelite" : 0,
        "modePaiement" : ticket["modePaiement"],
        "articles" : [
        ]
    }

    card = ""
    if "user" in ticket :
        new_sale["client"] = ticket["user"]
    if ticket["modePaiement"] == "CARD":
        card = ticket["card"]

    total_panier = 0
    for product_panier in ticket["panier"]:
        for product in products:
            # COMMENTER LE IF POUR PAS CHECK SI ON A LE PRODUIT
            if product_panier["codeProduit"] == product.codeProduit:
                new_created_product = calculatePrice(product, product_panier["quantity"], new_sale["client"])
                all_articles_calculated.append(new_created_product)
                total_panier += (new_created_product["prixApres"]) * product_panier["quantity"]
                new_sale["articles"].append(new_created_product)
    new_sale["prix"] = total_panier

    t1 = Tickets(date=new_sale["date"], prix=new_sale["prix"], client=new_sale["client"], pointsFidelite=new_sale["pointsFidelite"], modePaiement=new_sale["modePaiement"], articles=json.dumps(all_articles_calculated))
    t1.save()

    if total_panier != 0:
        return_tickets.append(new_sale)

        generated_body = {
            "client_id" : new_sale["client"],
            "payement_method": new_sale["modePaiement"],
            "card" : card,
            "credit_date" : "",
            "amount" : total_panier
        }
        generated_body = json.dumps(generated_body)
        generated_body = json.loads(generated_body)
        status, response = api.post_request2("gestion-paiement", "/api/proceed-payement", generated_body)

    return HttpResponse("done")

# Check if the product is in promo
def calculatePrice(product, quantity, client):
    return_product = {
        "codeProduit": product.codeProduit,
        "prix" : product.prix,
        "prixApres": 0,
        "promo": 0,
        "promo_client" : 0,
        "promo_client_produit" : 0,
        "quantity": quantity
    }

    difference = 0

    promotions = Promotion.objects.all()
    client_promotions = ClientPromotion.objects.all()
    product_client_promotions = PromotionsCustomersProducts.objects.all()
    for promo in promotions:
        if promo.codeProduit == product.codeProduit:
            return_product["promo"] = promo.reduction
            difference += promo.reduction * product.prix / 100

    for client_ in client_promotions:
        if (client_.IdClient == client):
            return_product["promo_client"] = client_.reduction
            difference += client_.reduction * product.prix / 100

    for client_promo in product_client_promotions:
        if (client_promo.IdClient == client and client_promo.codeProduit == product.codeProduit):
            return_product["promo_client_produit"] = client_promo.reduction
            difference += client_promo.reduction * product.prix / 100

    return_product["prixApres"] = product.prix - difference
    return return_product


def getTickets(request):
    tickets = Tickets.objects.all()
    tickets_returned = []
    for ticket in tickets:
        t1 = {
            "date" : ticket.date,
            "prix" : ticket.prix,
            "client" : ticket.client,
            "pointsFidelite" : ticket.pointsFidelite,
            "modePaiement" : ticket.modePaiement,
            "articles" : json.loads(ticket.articles)
        }

    return_response = {
        "tickets" : tickets_returned
    }
    
    return JsonResponse(return_response, safe=False)