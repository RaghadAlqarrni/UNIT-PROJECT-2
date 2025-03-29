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

def sign_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "البريد الإلكتروني موجود بالفعل.")
            return redirect('app_main:verify_otp')  

        user = CustomUser(
            username=email.split('@')[0],  
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )
        user.set_password("password123")  
        user.save()

        send_otp(phone_number)  
        messages.success(request, "تم التسجيل بنجاح! تم إرسال رمز التحقق إلى هاتفك.")
        return redirect('app_main:verify_otp')

    return render(request, 'app_main/sign.html')

def invester_view(request):
    return render(request, 'app_main/invester_detail.html')

def send_otp(phone_number):
    otp = random.randint(1000, 9999)
    cache.set(phone_number, otp, timeout=300)  

    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"رمز التحقق الخاص بك هو: {otp}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
    except Exception as e:
        print(f"خطأ في إرسال OTP: {e}")
    
    return otp

@login_required
def verify_otp(request):
    user = request.user
    stored_otp = cache.get(user.phone_number)

    if request.method == "POST":
        entered_otp = request.POST.get("otp")

        if stored_otp and str(stored_otp) == entered_otp:
            user.is_phone_verified = True  
            user.save()
            messages.success(request, "تم التحقق من رقم الهاتف بنجاح!")
            return redirect("app_main:main_view")
        else:
            messages.error(request, "رمز التحقق غير صحيح أو منتهي الصلاحية.")

    return render(request, "app_main/verify_otp.html")

@login_required
def request_otp(request):
    send_otp(request.user.phone_number)
    messages.info(request, "تم إرسال رمز التحقق إلى هاتفك.")
    return redirect(request, "app_main:verify_otp")

def login_view(request):
    return render(request, "app_main/login.html")


def business_signup(request):
    return render(request, "app_main/business_signup.html")



def contact(request):

     if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

       
        contact_message = ContactMessage(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        contact_message.save()

        messages.success(request, "Your message has been sent successfully!")
        return redirect('app_main:contact')  
     return render(request, 'app_main/contect.html')

def about_view(request):
    return render(request, 'app_main/about.html')






