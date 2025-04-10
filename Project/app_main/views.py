import random
from django.core.cache import cache
from django.conf import settings
from twilio.rest import Client
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django.core.exceptions import ValidationError

def main_view(request):
    
    if request.user.is_authenticated:
        print(request.user.email)
    else:
        print("User is not logged in")

    return render(request, 'app_main/index.html')

def invester_view(request):
    return render(request, 'app_main/invester_detail.html')


def contact(request:HttpRequest):
    
    if request.method == "POST":
        contact = Contact(full_name=request.POST["full_name"], email=request.POST["email"], message=request.POST["message"], subject=request.POST["subject"])
        contact.save()

        
        content_html = render_to_string("app_main/mail/confirmation.html")
        send_to = contact.email
        email_message = EmailMessage("confiramation", content_html, settings.EMAIL_HOST_USER, [send_to])
        email_message.content_subtype = "html"
        
        email_message.send()

        messages.success(request, "Thank You for checking my website.", "alert-success")

    return render(request, 'app_main/contact.html' )



def about_view(request):
    return render(request, 'app_main/about.html')








