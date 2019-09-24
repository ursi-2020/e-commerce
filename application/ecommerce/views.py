import sys

from django.http import HttpResponse
from apipkg import api_manager as api
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django import forms

from . import models

import json

def index(request):
    time = api.send_request('scheduler', 'clock/time')
    return HttpResponse("L'heure de la clock est %r" % time)


# Print HelloWorld
def helloWolrd(request):
    if request.method != "GET":
        return HttpResponse("Forbidden")
    print(request)
    return HttpResponse("Hello World ! :)\n")


# POST request - print payload
@csrf_exempt
def printJson(request):
    if request.method != "POST":
        return HttpResponse("Forbidden")
    jsonBody = json.loads(request.body)
    return HttpResponse(jsonBody["app_name"] + " : " + jsonBody["message"])


# Display form
def displayForm(request):
    info = api.send_request("gestion-paiement", "ihm")
    print(info)
    name = forms.TextInput(attrs={'size': 10, 'title': 'Your name'})
    return render(request, 'form.html')

# Search after validation button
def search(request):
    if request.method == 'POST':
        print(request.POST.get('textfield', None))
        return HttpResponse(request.POST.get('textfield', None))
    else:
        return render(request, 'form.html')

# Save from DB
def saveDB(request):
    models.Article.objects.create(nom='Apple', stock=1)
    return HttpResponse("Saved")

# Read from DB
def readDB(request):
    return HttpResponse(models.Article.objects.values_list())


def getInfo(request):
    return HttpResponse(api.send_request("gestion-paiement", "ihm"))

# Clear DB
# def removeDB(request):
#     models.Article.objects.all().delete()
#     return HttpResponse("Models removed")