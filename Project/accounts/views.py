from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import InvestorSignUpForm, BusinessSignUpForm
from .models import *
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db import transaction

def investor_signup(request):
    if request.method == 'POST':
        form = InvestorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
           
            InvestorProfile.objects.create(
                user=user,
                investment_preferences=form.cleaned_data['investment_preferences'],
                portfolio_size=form.cleaned_data['portfolio_size']
            )
            login(request, user)
            return redirect('app_main:main_view')
    else:
        form = InvestorSignUpForm()
    return render(request, 'accounts/investor_signup.html', {'form': form})

def business_signup(request):
    if request.method == 'POST':
        form = BusinessSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            
            BusinessProfile.objects.create(
                user=user,
                company_name=form.cleaned_data['company_name'],
                company_description=form.cleaned_data['company_description'],
                industry=form.cleaned_data['industry']
            )
            login(request, user)
            return redirect('app_main:main_view')
    else:
        form = BusinessSignUpForm()
    return render(request, 'accounts/business_signup.html', {'form': form})

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('app_main:main_view')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/signin.html')


@login_required
def profile(request, user_name):

    try:
        user = User.objects.get(username=user_name)
        if not Profile.objects.filter(user=user).first():
            new_profile = Profile(user=user)
            new_profile.save()

    except Exception as e:
        print(e)
    
    return render(request, 'accounts/profile.html', {"user" : user})


@login_required
def edit_profile(request):
    user = request.user
    profile = None
    profile_type = None

    if hasattr(user, 'investor_profile'):
        profile = user.investor_profile
        profile_type = 'investor'
    elif hasattr(user, 'business_profile'):
        profile = user.business_profile
        profile_type = 'business'

    if request.method == 'POST':
        
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()

        
        if profile_type == 'investor':
            profile.investment_preferences = request.POST.get('investment_preferences', profile.investment_preferences)
            profile.portfolio_size = request.POST.get('portfolio_size', profile.portfolio_size)
            profile.save()
        elif profile_type == 'business':
            profile.company_name = request.POST.get('company_name', profile.company_name)
            profile.industry = request.POST.get('industry', profile.industry)
            profile.project_name = request.POST.get('project_name', profile.project_name)
            profile.funding_required = request.POST.get('funding_required', profile.funding_required)
            profile.description = request.POST.get('description', profile.description)
            profile.save()

        messages.success(request, 'تم تحديث الملف الشخصي بنجاح')
        return redirect('accounts:profile')

    context = {
        'user': user,
        'profile': profile,
        'profile_type': profile_type
    }
    return render(request, 'accounts/edit_profile.html', context)




@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()  
            update_session_auth_hash(request, user)  
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:profile') 
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)  

    return render(request, 'accounts/change_password.html', {'form': form})

def sign_out(request):
    logout(request)
    return redirect('app_main:main_view') 

def signup_view(request):
    if request.method == "POST":
        user_type = request.POST.get("user_type")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("accounts:sign_up")

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1
                )

                if user_type == "investor":
                    InvestorProfile.objects.create(
                        user=user,
                        id_number=request.POST.get("id_number"),
                        first_name=request.POST.get("first_name"),
                        middle_name=request.POST.get("middle_name"),
                        last_name=request.POST.get("last_name"),
                        investment_preferences=request.POST.get("investment_preferences"),
                        portfolio_size=request.POST.get("portfolio_size"),
                        income_sources=request.POST.get("income_sources"),
                        employment_status=request.POST.get("employment_status"),
                        monthly_income=request.POST.get("monthly_income"),
                        beneficial_owner=request.POST.get("beneficial_owner") == "on",
                        investor_type=request.POST.get("investor_type"),
                        investment_size=request.POST.get("investment_size"),
                        sector=request.POST.get("sector"),
                )


                elif user_type == "business":
                    BusinessProfile.objects.create(
                        user=user,
                        project_name=request.POST.get("project_name"),
                        company_name=request.POST.get("company_name"),
                        founder_name=request.POST.get("founder_name"),
                        registration_number=request.POST.get("registration_number"),
                        business_location=request.POST.get("business_location"),
                        start_date=request.POST.get("start_date"),
                        description=request.POST.get("description"),
                        sector=request.POST.get("sector"),
                        funding_required=request.POST.get("funding_required"),
                        equity_offered=request.POST.get("equity_offered"),
                        expected_roi=request.POST.get("expected_roi"),
                        revenue_model=request.POST.get("revenue_model"),
                        projected_revenue=request.POST.get("projected_revenue"),
                        business_plan=request.FILES.get("business_plan"),
                        project_image=request.FILES.get("project_image"),
                        registration_document=request.FILES.get("registration_document"),
                        pitch_deck=request.FILES.get("pitch_deck"),
                    )

                messages.success(request, "Account created successfully! You can now sign in.")
                return redirect("accounts:sign_in")

        except Exception as e:
            messages.error(request, f"Something went wrong: {e}")
            return redirect("accounts:sign_up")

    return render(request, "accounts/signup.html")