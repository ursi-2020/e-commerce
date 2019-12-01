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

def createCustomer(request):
    print('ok')
    return HttpResponse("done")


def salesSimulation(request):
    return HttpResponse("done")
