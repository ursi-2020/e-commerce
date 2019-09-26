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

def index(request):
   #time = api.send_request('scheduler', 'clock/time')
   #return HttpResponse("L'heure de la clock est %r" % time)
   return render(request, 'index.html')


# Print HelloWorld
#def helloWolrd(request):
    #    if request.method != "GET":
    #    return HttpResponse("Forbidden")
    #print(request)
    #return HttpResponse("Hello World ! :)\n")


# POST request - print payload
#@csrf_exempt
#def printJson(request):
    #    if request.method != "POST":
    #    return HttpResponse("Forbidden")
    #jsonBody = json.loads(request.body)
    #return HttpResponse(jsonBody["app_name"] + " : " + jsonBody["message"])


# Display form
#def displayForm(request):
#    info = api.send_request("gestion-paiement", "ihm")
#    print(info)
#    name = forms.TextInput(attrs={'size': 10, 'title': 'Your name'})
#    return render(request, 'form.html')

def connect(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    print(username)
    print(password)
    body = {
        'firstName' : username,
        'lastName' : password
    }
    signup = api.post_request("crm", "/api/update_db", json.dumps(body))
    print(signup)
    return render(request, 'products.html')

def displayProducts(request):
    if request.method == "GET":
        products = api.send_request("catalogue-produit", "catalogueproduit/api/data")
        print(products)
        data = json.loads(products)
        for produit in data['produits']:
            p = Produit(codeProduit=produit['codeProduit'], familleProduit=produit['familleProduit'],
                        descriptionProduit=produit['descriptionProduit'], prix=produit['prix'], quantiteMin=1, packaging=0)
            p.save()
    return JsonResponse({'data': products})

# Search after validation button
#def search(request):
    #    if request.method == 'POST':
    #    print(request.POST.get('textfield', None))
    #   return HttpResponse(request.POST.get('textfield', None))
    #else:
#   return render(request, 'form.html')

# Save from DB
#def saveDB(request):
    #    models.Article.objects.create(nom='Apple', stock=1)
    #return HttpResponse("Saved")

# Read from DB
def readDB(request):
    return HttpResponse(models.Produit.objects.values_list())


#def getInfo(request):
#   return HttpResponse(api.send_request("gestion-paiement", "ihm"))

# Clear DB
def removeDB(request):
     models.Produit.objects.all().delete()
     return HttpResponse("Models removed")