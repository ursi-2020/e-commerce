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
from .. import models
from datetime import datetime, timedelta

import json
import requests


# Return all tickets
def getTickets(request):
    data = {
        "tickets": [
              {
                "id": 42,
                "date": "2019-10-09T17:01:29.408701Z",
                "prix": 424,
                "client": "a14e39ce-e29e-11e9-a8cb-08002751d198",
                "pointsFidelite": 0,
                "modePaiement": "CASH",
                "articles": [
                  {
                    "codeProduit": "X1-0",
                    "prix" : 800,
                    "prixApres": 400,
                    "promo": 50,
                    "quantity": 2
                  },
                  {
                    "codeProduit": "X1-9",
                    "prix" : 48,
                    "prixApres": 24,
                    "promo": 50,
                    "quantity": 1
                  }
                ]
              },
              {
                "id": 38,
                "date": "2019-10-09T18:03:45.408701Z",
                "prix": 7582,
                "client": "a14e39ce-e29e-11e9-a8cb-08002751d198",
                "pointsFidelite": 18,
                "modePaiement": "CARD",
                "articles": [
                  {
                    "codeProduit": "X1-4",
                    "prix" : 36,
                    "prixApres": 18,
                    "promo": 50,
                    "quantity": 2
                  }
                ]
              }
          ]
    }
    return JsonResponse(data)