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
    print('ok')
    print(request)
    return HttpResponse("done")

@csrf_exempt
def salesSimulation(request):
    return HttpResponse("done")


def testSales(request):
    data = {
        "success": "true",
        "result": "ok, 17 tickets generated",
        "tickets": [
            {
                "caisse": "3",
                "panier": [
                    {
                        "codeProduit": "X1-0",
                        "description": "Livre:P2-43",
                        "quantity": 1
                    }
                ],
                "modePaiement": "CARD",
	            "card":"BKN1CST18" 
            },
            {
                "caisse": "1",
                "panier": [
                    {
                        "codeProduit": "X1-3",
                        "description": "TV:P2-48",
                        "quantity": 1
                    },
                    {
                        "codeProduit": "X1-1",
                        "description": "TV:P1-13",
                        "quantity": 2
                    },
                    {
                        "codeProduit": "X1-10",
                        "description": "Livre:P2-39",
                        "quantity": 1
                    }
                ],
                "modePaiement": "CASH"
            },
            {
                "caisse": "2",
                "panier": [
                    {
                        "codeProduit": "X1-0",
                        "description": "Frigos:P1-18",
                        "quantity": 1
                    },
                    {
                        "codeProduit": "X1-10",
                        "description": "Console:P2-46",
                        "quantity": 2
                    },
                    {
                        "codeProduit": "X1-8",
                        "description": "Console:P2-14",
                        "quantity": 2
                    }
                ],
                "carteFid": "259a3a6c-1296-11ea-b6f4-08002751d198",
                "modePaiement": "CARD",
                "card": "BKN1CST17"
            },
            {
                "caisse": "4",
                "panier": [
                    {
                        "codeProduit": "X1-8",
                        "description": "Console:P3-24",
                        "quantity": 1
                    },
                    {
                        "codeProduit": "X1-10",
                        "description": "DVD:P2-34",
                        "quantity": 1
                    },
                    {
                        "codeProduit": "X1-3",
                        "description": "Console:P2-27",
                        "quantity": 1
                    },
                    {
                        "codeProduit": "X1-0",
                        "description": "DVD:P2-12",
                        "quantity": 1
                    }
                ],
                "modePaiement": "CASH"
            },
            {
                "caisse": "2",
                "panier": [
                    {
                        "codeProduit": "X1-0",
                        "description": "Frigos:P1-18",
                        "quantity": 1
                    },
                    {
                        "codeProduit": "X1-1",
                        "description": "Console:P2-46",
                        "quantity": 1
                    },
                    {
                        "codeProduit": "X1-3",
                        "description": "Console:P2-14",
                        "quantity": 1
                    }
                ],
                "carteFid": "259ab73a-1296-11ea-b6f4-08002751d198",
                "modePaiement": "CARD",
                "card": "BKN1CST17"
            },
            {
                "caisse": "2",
                "panier": [
                    {
                        "codeProduit": "X1-0",
                        "description": "Frigos:P1-18",
                        "quantity": 2
                    },
                    {
                        "codeProduit": "X1-1",
                        "description": "Console:P2-46",
                        "quantity": 1
                    },
                    {
                        "codeProduit": "X1-8",
                        "description": "Console:P2-14",
                        "quantity": 2
                    }
                ],
                "carteFid": "259b09ba-1296-11ea-b6f4-08002751d198",
                "modePaiement": "CARD",
                "card": "BKN1CST17"
            },
            {
                "caisse": "2",
                "panier": [
                    {
                        "codeProduit": "X1-0",
                        "description": "Frigos:P1-18",
                        "quantity": 3
                    },
                    {
                        "codeProduit": "X1-10",
                        "description": "Console:P2-46",
                        "quantity": 1
                    },
                    {
                        "codeProduit": "X1-3",
                        "description": "Console:P2-14",
                        "quantity": 1
                    }
                ],
                "carteFid": "259ab73a-1296-11ea-b6f4-08002751d198",
                "modePaiement": "CARD",
                "card": "BKN1CST17"
            },
            {
                "caisse": "2",
                "panier": [
                    {
                        "codeProduit": "X1-0",
                        "description": "Frigos:P1-18",
                        "quantity": 4
                    },
                    {
                        "codeProduit": "X1-10",
                        "description": "Console:P2-46",
                        "quantity": 2
                    },
                    {
                        "codeProduit": "X1-8",
                        "description": "Console:P2-14",
                        "quantity": 2
                    }
                ],
                "carteFid": "259a3a6c-1296-11ea-b6f4-08002751d198",
                "modePaiement": "CARD",
                "card": "BKN1CST17"
            }
        ]
    }
    tickets = {
        "tickets" : [

        ]
    }
    data = json.dumps(data)
    data = json.loads(data)
    tickets = data["tickets"]
    products = Produit.objects.all()

    promotions = Promotion.objects.all()
    client_promotions = ClientPromotion.objects.all()
    product_promotions = PromotionsCustomersProducts.objects.all()
    for ticket in tickets:
        carteFid = ""
        if "carteFid" in ticket :
            carteFid = ticket["carteFid"]
        modePaiement = ticket["modePaiement"]
        card = ""
        if modePaiement == "CARD":
            card = ticket["card"]
        for product_panier in ticket["panier"]:
            for product in products:
                if product_panier["codeProduit"] == product.codeProduit:
                    print("c'est ok ! " + str(product.codeProduit))
    return HttpResponse("done")