
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

from .api import *
from .crm import *
from .products import *
from .scheduler import *
from .simulator import *

def index(request):
   #time = api.send_request('scheduler', 'clock/time')
   #return HttpResponse("L'heure de la clock est %r" % time)
   r = requests.post('http://127.0.0.1:5001/register', data={'app': 'ecommerce',
                                                              'path': '/mnt/technical_base/e-commerce/received_files',
                                                              'route': 'http://127.0.0.1:9020/notifier'})

   # r = requests.post('http://127.0.0.1:5001/unregister', data={'app': 'ecommerce'})
   return render(request, 'index.html')