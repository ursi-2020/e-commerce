import sys

from django.http import HttpResponse
from apipkg import api_manager as api
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    time = api.send_request('scheduler', 'clock/time')
    return HttpResponse("L'heure de la clock est %r" % time)


def helloWolrd(request):
    if request.method != "GET":
        return HttpResponse("Forbidden")
    print(request)
    return HttpResponse("Hello World ! :)\n")


@csrf_exempt
def printJson(request):
    if request.method != "POST":
        return HttpResponse("Forbidden")
    jsonBody = json.loads(request.body)
    return HttpResponse(jsonBody["app_name"] + " : " + jsonBody["message"])