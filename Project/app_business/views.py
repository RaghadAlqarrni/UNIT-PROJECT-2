from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
# Create your views here.

def business_detail_view(request):
    return render(request, 'app_business/business_detail.html')

def business_signup_view(request):
    return render(request, 'app_business/business_signup.html')














