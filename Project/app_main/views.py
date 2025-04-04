import random
from django.core.cache import cache
from django.conf import settings
from twilio.rest import Client
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.core.exceptions import ValidationError

def main_view(request):
    return render(request, 'app_main/index.html')

def invester_view(request):
    return render(request, 'app_main/invester_detail.html')


def contact(request):
     return render(request, "app_main/contact.html")



def about_view(request):
    return render(request, 'app_main/about.html')






