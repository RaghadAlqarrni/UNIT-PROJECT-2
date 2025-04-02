from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, transaction
from django.contrib import messages

def sign_up(request: HttpRequest):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        email = request.POST.get("email", "").strip()
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()

        if not username or not password or not email:
            messages.error(request, "All fields are required", "alert-danger")
            return redirect("accounts:sign_up")

        try:
            with transaction.atomic():
                new_user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
                new_user.save()
            messages.success(request, "User registered successfully!", "alert-success")
            return redirect("accounts:sign_in")
        
        except IntegrityError:
            messages.error(request, "Username is already taken. Choose another one.", "alert-danger")
        except Exception as e:
            messages.error(request, "An error occurred. Please try again.", "alert-danger")
            print(f"Error: {e}")

    return render(request, "accounts/signup.html")


def sign_in(request: HttpRequest):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if not username or not password:
            messages.error(request, "Username and password are required", "alert-danger")
            return redirect("accounts:sign_in")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged in successfully!", "alert-success")
            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request, "Invalid credentials. Try again.", "alert-danger")

    return render(request, "accounts/signin.html")


def log_out(request: HttpRequest):
    logout(request)
    messages.success(request, "Logged out successfully.", "alert-warning")
    return redirect(request.GET.get("next", "/"))
