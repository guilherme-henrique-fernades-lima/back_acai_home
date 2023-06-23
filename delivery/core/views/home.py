from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
import requests, json


def index(request):

    return render(request, "index.html")
