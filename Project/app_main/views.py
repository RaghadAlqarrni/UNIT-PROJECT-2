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
from django.shortcuts import render
from accounts.models import BusinessProfile
from xhtml2pdf import pisa
from io import BytesIO


def main_view(request):
    
    latest_projects = BusinessProfile.objects.order_by('-id')[:2]

    
    if request.user.is_authenticated:
        print(f"Logged in user: {request.user.email}")
    else:
        print("User is not logged in")

    return render(request, 'app_main/index.html', {
        'projects': latest_projects
    })


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




def send_investment_contract(user, project, amount):
    html = render_to_string("pdf_templates/investment_contract.html", {
        'user_name': user.get_full_name(),
        'project_name': project.project_name,
        'investment_amount': amount,
        'date': timezone.now().date()
    })

    result = BytesIO()
    pisa.CreatePDF(html, dest=result)

    email = EmailMessage(
        subject="Investment Confirmation - Namaa",
        body="Thank you for your investment. Please find the attached confirmation document.",
        to=[user.email]
    )
    email.attach('investment_contract.pdf', result.getvalue(), 'application/pdf')
    email.send()









