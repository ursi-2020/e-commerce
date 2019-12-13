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

@csrf_exempt
def createCustomer(request):
    # body_unicode = request.body.decode('latin-1')
    # body = json.loads(body_unicode)
    # print(body)
    # print(body["Nom"])
    # nom = body["Nom"]
    # print(body["Prenom"])
    # print(body["email"])
    # print(body["Credit"])
    # print(body["Paiement"])

    # generated_body = {

    # }
    # if "Compte" in body :
    #     generated_body = {
    #         "Nom" : nom,
    #         "Prenom" : body["Prenom"],
    #         "email" : body["email"],
    #         "Credit" : body["Credit"],
    #         "Paiement" : body["Paiement"],
    #         "Compte" : body["Compte"]
    #     }
    # else :
    #     generated_body = {
    #         "Nom" : nom,
    #         "Prenom" : body["Prenom"],
    #         "email" : body["email"],
    #         "Credit" : (body["Credit"]),
    #         "Paiement" : body["Paiement"],
    #         "Compte" : ""
    #     }
    


    # print(generated_body)
    
    # generated_body = json.dumps(generated_body)
    # generated_body = json.loads(generated_body)
    # signup = api.post_request("crm", "/api/create_customer", generated_body)


    # info = json.loads(signup)
    # print(signup)

    # return JsonResponse({
    #     "CarteFid" : info["idClient"]
    # })

    return JsonResponse({
        "CarteFid" : "16"
    })

@csrf_exempt
def salesSimulation(request):
    print("inside sales simulation")
    body_unicode = request.body.decode('latin-1')
    body = json.loads(body_unicode)
    print(body)
    return HttpResponse("done")


# def testSales(request):
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

    # data = json.dumps(data)
    # data = json.loads(data)

    # # Tickets array
    # tickets = data["tickets"]

    # # Retrieve products
    # products = Produit.objects.all()


    # for ticket in tickets:
    #     # Variable declaration
    #     new_sale = {
    #         "date" = datetime.now()
    #         "prix" = 0
    #         "client" = ""
    #         "pointsFidelite" = 0
    #         "modePaiement" = ticket["modePaiement"]
    #         "articles" = [
    #         ]
    #     }
    #     card = ""
    #     carteFid = ""

    #     if "carteFid" in ticket :
    #         carteFid = ticket["carteFid"]
    #     if modePaiement == "CARD":
    #         card = ticket["card"]

    #     for product_panier in ticket["panier"]:
    #         for product in products:
    #             if product_panier["codeProduit"] == product.codeProduit:
    #                 print("c'est ok ! " + str(product.codeProduit))
                    

    # return HttpResponse("done")

# Check if the product is in promo
# def isInPromo(product): 
#     promotions = Promotion.objects.all()
#     client_promotions = ClientPromotion.objects.all()
#     product_promotions = PromotionsCustomersProducts.objects.all()

