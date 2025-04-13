from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from .models import *
from .forms import *
from wallet.models import Payment
from django.db.models import Sum

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO


from django.core.mail import send_mail

def send_investment_contract(user, project, amount):
    subject = "Investment Confirmation - Namaa"
    message = f"""
Dear {user.get_full_name()},

Thank you for investing in "{project.project_name}".

We confirm that your investment of ${amount} has been successfully added to the project.

Project Summary:
- Sector: {project.sector}
- Location: {project.business_location}
- Expected ROI: {project.expected_roi}%
- Equity Offered: {project.equity_offered}%

You can track your investment anytime by logging into your dashboard.

Thank you for using Namaa.

Best regards,  
Namaa Team
"""
    from_email = "noreply@namaa.com"
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)



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
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('accounts:sign_up')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('accounts:sign_up')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        if user_type == 'investor':
            profile = InvestorProfile.objects.create(
                user=user,
                roi=0.0,
                level='Newbie',
                employment_status=request.POST.get('employment_status'),
                preferred_investment_type=request.POST.get('preferred_investment_type'),
                investment_duration=request.POST.get('investment_duration'),
                industries_of_interest=request.POST.get('industries_of_interest'),
                investment_size=request.POST.get('investment_size'),
            )
            profile.save()
        elif user_type == 'business':
            profile = BusinessProfile.objects.create(
                user=user,
                project_name=request.POST.get('project_name'),
                company_name=request.POST.get('company_name'),
                founder_name=request.POST.get('founder_name'),
                registration_number=request.POST.get('registration_number'),
                business_location=request.POST.get('business_location'),
                start_date=request.POST.get('start_date') or None,
                description=request.POST.get('description'),
                sector=request.POST.get('sector_business'),
                funding_required=request.POST.get('funding_required') or 0.0,
                equity_offered=request.POST.get('equity_offered') or 0.0,
                expected_roi=request.POST.get('expected_roi') or 0.0,
                revenue_model=request.POST.get('revenue_model'),
                projected_revenue=request.POST.get('projected_revenue'),
                business_plan=request.FILES.get('business_plan'),
                project_image=request.FILES.get('project_image'),
                registration_document=request.FILES.get('registration_document'),
                pitch_deck=request.FILES.get('pitch_deck'),
            )
            profile.save()

        login(request, user)
        return redirect('app_main:main_view')

    return render(request, 'accounts/signup.html')


@login_required
def investor_dashboard(request):
    try:
        investor = InvestorProfile.objects.get(user=request.user)
    except InvestorProfile.DoesNotExist:
        messages.error(request, "You are not registered as an investor.")
        return redirect('app_main:main_view')

    investments = Investment.objects.filter(investor=investor).select_related('project')
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')[:5]

    for inv in investments:
        inv.project.funding_percentage = (inv.project.amount_raised / inv.project.funding_required) * 100

    return render(request, 'accounts/Investor_dashboard.html', {
        'investor': investor,
        'investments': investments,
        'notifications': notifications,
    })


def send_notification(user, message):
    Notification.objects.create(user=user, message=message)

@login_required
def business_profile_view(request):
   
    profile = get_object_or_404(BusinessProfile, user=request.user)

    
    funding_percentage = profile.funding_percentage()

    
    return render(request, 'accounts/business_owner_profile.html', {
        'profile': profile,
        'funding_percentage': funding_percentage,
    })

@login_required
def invest_in_project(request, project_id):
    
    project = get_object_or_404(BusinessProfile, id=project_id)

    
    try:
        investor = InvestorProfile.objects.get(user=request.user)
    except InvestorProfile.DoesNotExist:
        messages.error(request, "This action is only available for investors.")
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.investor = investor
            investment.project = project

            
            total_balance = Payment.objects.filter(user=request.user, is_successful=True).aggregate(Sum('amount'))['amount__sum'] or 0

            if investment.amount > total_balance:
                messages.error(request, "You don't have enough balance in your wallet.")
                return redirect('wallet:wallet_view')

            investment.save()
            project.amount_raised += investment.amount
            project.save()

            Notification.objects.create(
                user=request.user,
                message=f"Your investment of {investment.amount} has been added to {project.project_name}."
            )
            send_investment_contract(request.user, project, investment.amount)

            messages.success(request, "Investment completed successfully.")
            return redirect('accounts:investor_dashboard')
    else:
        form = InvestmentForm()

    return render(request, 'accounts/invest.html', {'form': form, 'project': project})

def profile(request):
    if hasattr(request.user, 'businessprofile'):
        return redirect('accounts:business_dashboard')
    elif hasattr(request.user, 'investorprofile'):
        return redirect('accounts:investor_dashboard')
    else:
        messages.warning(request, "No profile associated with this user.")
        return redirect('accounts:sign_up')