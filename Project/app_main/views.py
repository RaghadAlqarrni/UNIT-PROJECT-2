from django.shortcuts import render

# Create your views here.


def main_view(request):
    return render(request, 'app_main/index.html')


def sign_view(request):
    return render(request, 'app_main/sign.html')
