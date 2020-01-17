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


# Display scheduler page
# Get info and scheduled tasks list
def displayScheduler(request):
    info = api.send_request("scheduler", "clock/info")
    tasks = api.send_request("scheduler", "schedule/list")
    info = json.loads(info)
    info = {
        "data" : info,
        "tasks" : tasks
    }
    return render(request, "scheduler.html", info)


# Add a task to scheduler using the form
def addTaskScheduler(request):
    data = request.POST.dict()
    time = datetime.strptime(data["time"], '%Y-%m-%dT%H:%M')
    host = ""
    recurrence = data["recurrence"]
    url = ""
    source = "e-commerce"
    name = "get_customers"
    data2 = ""
    if data["app"] == "products":
        host = "e-commerce"
        url = "ecommerce/add-auto"
        name = "get_products"
    elif data["app"] == "crm":
        host = "e-commerce"
        url = "ecommerce/auto_load_customers"
        name = "get_customers"
    schedule_task(host, url, time, recurrence, data2, source, name)

    info = api.send_request("scheduler", "clock/info")
    tasks = api.send_request("scheduler", "schedule/list")
    info = json.loads(info)
    info = {
        "data" : info,
        "tasks" : tasks
    }
    return render(request, "scheduler.html", info)


# Function used to schedule a task
def schedule_task(host, url, time, recurrence, data, source, name):
    time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
    headers = {'Host': 'scheduler'}
    data = {"target_url": url, "target_app": host, "time": time_str, "recurrence": recurrence, "data": data, "source_app": source, "name": name}
    r = requests.post(api.api_services_url + 'schedule/add', headers = headers, json = data)
    return r.text


# Remove all tasks from scheduler
@csrf_exempt
def removeAllTasks(request):
    remove = api.post_request("scheduler", "app/delete?source=ecommerce", '{source: "ecommerce"}')
    print(remove)
    return HttpResponse("done")