import random
from twilio.rest import Client
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
# Create your views here.


TWILIO_ACCOUNT_SID = "your_twilio_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_PHONE_NUMBER = "+1234567890"



otp_storage = {}

def send_otp(phone_number):
    otp = random.randint(100000, 999999) 
    otp_storage[phone_number] = otp 

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your OTP code is {otp}",
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return otp

def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        
        if user:
            request.session["phone_number"] = user.phone_number 
            send_otp(user.phone_number) 
            return redirect("verify_otp")  
        else:
            messages.error(request, "Invalid email or password.")
    
    return render(request, "login.html")

@login_required
def verify_otp_view(request):
    if request.method == "POST":
        phone_number = request.session.get("phone_number")
        entered_otp = request.POST.get("otp")
        
        if phone_number and otp_storage.get(phone_number) == int(entered_otp):
            del otp_storage[phone_number] 
            return redirect("main_view")  
        else:
            messages.error(request, "Invalid OTP. Please try again.")
    
    return render(request, "verify_otp.html")

def main_view(request):
    return render(request, 'app_main/index.html')


def sign_view(request):
    return render(request, 'app_main/sign.html')

@login_required
def resend_otp(request):
    phone_number = request.session.get("phone_number")
    
    if phone_number:
        send_otp(phone_number)
        messages.success(request, "A new OTP has been sent.")
    
    return redirect("verify_otp")