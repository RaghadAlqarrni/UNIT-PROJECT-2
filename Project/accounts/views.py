from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import InvestorSignUpForm, BusinessSignUpForm
from .models import InvestorProfile, BusinessProfile
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout

def investor_signup(request):
    if request.method == 'POST':
        form = InvestorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # إنشاء ملف المستثمر
            InvestorProfile.objects.create(
                user=user,
                investment_preferences=form.cleaned_data['investment_preferences'],
                portfolio_size=form.cleaned_data['portfolio_size']
            )
            login(request, user)
            return redirect('home')
    else:
        form = InvestorSignUpForm()
    return render(request, 'accounts/investor_signup.html', {'form': form})

def business_signup(request):
    if request.method == 'POST':
        form = BusinessSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # إنشاء ملف صاحب العمل
            BusinessProfile.objects.create(
                user=user,
                company_name=form.cleaned_data['company_name'],
                company_description=form.cleaned_data['company_description'],
                industry=form.cleaned_data['industry']
            )
            login(request, user)
            return redirect('home')
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
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/signin.html')


@login_required
def profile(request):
    user = request.user
    context = {}
    
    if hasattr(user, 'investor_profile'):
        context['profile'] = user.investor_profile
        context['profile_type'] = 'investor'
    elif hasattr(user, 'business_profile'):
        context['profile'] = user.business_profile
        context['profile_type'] = 'business'
    
    return render(request, 'accounts/profile.html', context)



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
        # تحديث بيانات المستخدم الأساسية
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()

        # تحديث بيانات البروفايل حسب النوع
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
            # Update session to prevent logout after password change
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