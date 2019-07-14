from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hello', views.helloWolrd, name='hello'),
    path('print', views.printJson, name='print'),
]