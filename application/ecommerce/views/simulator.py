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
from .. import models
from datetime import datetime, timedelta


import json
import requests

all_tickets = []

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
    # data = {
    #     "success": "true",
    #     "result": "ok, 17 tickets generated",
    #     "tickets": [
    #         {
    #             "caisse": "3",
    #             "panier": [
    #                 {
    #                     "codeProduit": "X1-0",
    #                     "description": "Livre:P2-43",
    #                     "quantity": 1
    #                 }
    #             ],
    #             "modePaiement": "CARD",
	#             "card":"BKN1CST18" 
    #         },
    #         {
    #             "caisse": "1",
    #             "panier": [
    #                 {
    #                     "codeProduit": "X1-3",
    #                     "description": "TV:P2-48",
    #                     "quantity": 1
    #                 },
    #                 {
    #                     "codeProduit": "X1-1",
    #                     "description": "TV:P1-13",
    #                     "quantity": 2
    #                 },
    #                 {
    #                     "codeProduit": "X1-10",
    #                     "description": "Livre:P2-39",
    #                     "quantity": 1
    #                 }
    #             ],
    #             "modePaiement": "CASH"
    #         },
    #         {
    #             "caisse": "2",
    #             "panier": [
    #                 {
    #                     "codeProduit": "X1-0",
    #                     "description": "Frigos:P1-18",
    #                     "quantity": 1
    #                 },
    #                 {
    #                     "codeProduit": "X1-10",
    #                     "description": "Console:P2-46",
    #                     "quantity": 2
    #                 },
    #                 {
    #                     "codeProduit": "X1-8",
    #                     "description": "Console:P2-14",
    #                     "quantity": 2
    #                 }
    #             ],
    #             "carteFid": "259a3a6c-1296-11ea-b6f4-08002751d198",
    #             "modePaiement": "CARD",
    #             "card": "BKN1CST17"
    #         },
    #         {
    #             "caisse": "4",
    #             "panier": [
    #                 {
    #                     "codeProduit": "X1-8",
    #                     "description": "Console:P3-24",
    #                     "quantity": 1
    #                 },
    #                 {
    #                     "codeProduit": "X1-10",
    #                     "description": "DVD:P2-34",
    #                     "quantity": 1
    #                 },
    #                 {
    #                     "codeProduit": "X1-3",
    #                     "description": "Console:P2-27",
    #                     "quantity": 1
    #                 },
    #                 {
    #                     "codeProduit": "X1-0",
    #                     "description": "DVD:P2-12",
    #                     "quantity": 1
    #                 }
    #             ],
    #             "modePaiement": "CASH"
    #         },
    #         {
    #             "caisse": "2",
    #             "panier": [
    #                 {
    #                     "codeProduit": "X1-0",
    #                     "description": "Frigos:P1-18",
    #                     "quantity": 1
    #                 },
    #                 {
    #                     "codeProduit": "X1-1",
    #                     "description": "Console:P2-46",
    #                     "quantity": 1
    #                 },
    #                 {
    #                     "codeProduit": "X1-3",
    #                     "description": "Console:P2-14",
    #                     "quantity": 1
    #                 }
    #             ],
    #             "carteFid": "259ab73a-1296-11ea-b6f4-08002751d198",
    #             "modePaiement": "CARD",
    #             "card": "BKN1CST17"
    #         },
    #         {
    #             "caisse": "2",
    #             "panier": [
    #                 {
    #                     "codeProduit": "X1-0",
    #                     "description": "Frigos:P1-18",
    #                     "quantity": 2
    #                 },
    #                 {
    #                     "codeProduit": "X1-1",
    #                     "description": "Console:P2-46",
    #                     "quantity": 1
    #                 },
    #                 {
    #                     "codeProduit": "X1-8",
    #                     "description": "Console:P2-14",
    #                     "quantity": 2
    #                 }
    #             ],
    #             "carteFid": "259b09ba-1296-11ea-b6f4-08002751d198",
    #             "modePaiement": "CARD",
    #             "card": "BKN1CST17"
    #         },
    #         {
    #             "caisse": "2",
    #             "panier": [
    #                 {
    #                     "codeProduit": "X1-0",
    #                     "description": "Frigos:P1-18",
    #                     "quantity": 3
    #                 },
    #                 {
    #                     "codeProduit": "X1-10",
    #                     "description": "Console:P2-46",
    #                     "quantity": 1
    #                 },
    #                 {
    #                     "codeProduit": "X1-3",
    #                     "description": "Console:P2-14",
    #                     "quantity": 1
    #                 }
    #             ],
    #             "carteFid": "259ab73a-1296-11ea-b6f4-08002751d198",
    #             "modePaiement": "CARD",
    #             "card": "BKN1CST17"
    #         },
    #         {
    #             "caisse": "2",
    #             "panier": [
    #                 {
    #                     "codeProduit": "X1-0",
    #                     "description": "Frigos:P1-18",
    #                     "quantity": 4
    #                 },
    #                 {
    #                     "codeProduit": "X1-10",
    #                     "description": "Console:P2-46",
    #                     "quantity": 2
    #                 },
    #                 {
    #                     "codeProduit": "X1-8",
    #                     "description": "Console:P2-14",
    #                     "quantity": 2
    #                 }
    #             ],
    #             "carteFid": "259a3a6c-1296-11ea-b6f4-08002751d198",
    #             "modePaiement": "CARD",
    #             "card": "BKN1CST17"
    #         }
    #     ]
    # }
    # tickets_to_send = [{
    #     "id": 42,
    #     "date": "2019-10-09T17:01:29.408701Z",
    #     "prix": 424,
    #     "client": "a14e39ce-e29e-11e9-a8cb-08002751d198",
    #     "pointsFidelite": 0,
    #     "modePaiement": "CASH",
    #     "articles": [
    #         {
    #             "codeProduit": "X1-0",
    #             "prix" : 800,
    #             "prixApres": 400,
    #             "promo": 50,
    #             "quantity": 2
    #         }
    #     ]
    # }]

    return_tickets = []

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
                total_panier += (new_created_product["prixApres"]) * product_panier["quantity"]
                new_sale["articles"].append(new_created_product)
    new_sale["prix"] = total_panier

    if total_panier != 0:
        all_tickets.append(new_sale)
        return_tickets.append(new_sale)
                        
        # #print(return_tickets)


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
    return_response = {
        "tickets" : all_tickets
    }
    return JsonResponse(return_response, safe=False)