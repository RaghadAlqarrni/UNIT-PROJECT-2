from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from accounts.models import *
from django.db.models import Sum
from django.contrib import messages

# Create your views here.


@login_required
def wallet_view(request):
    user = request.user

    total_deposits = Payment.objects.filter(user=user, is_successful=True).aggregate(Sum('amount'))['amount__sum'] or 0

    try:
        investor = InvestorProfile.objects.get(user=user)
        total_invested = Investment.objects.filter(investor=investor).aggregate(Sum('amount'))['amount__sum'] or 0
    except InvestorProfile.DoesNotExist:
        total_invested = 0

    wallet_balance = total_deposits - total_invested

    context = {
        'wallet_owner': user.username,
        'wallet_token': 231002,
        'wallet_balance': wallet_balance,
    }
    return render(request, 'wallet/wallet.html', context)



@login_required
def diposit(request):
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        card_name = request.POST.get('card_name')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        amount = request.POST.get('amount')

        if not all([card_number, card_name, expiry_date, cvv, amount]):
            messages.error(request, 'Please fill all fields')
            return redirect('wallet:diposit')

        try:
            payment = Payment(
                user=request.user,
                card_number=card_number,
                card_name=card_name,
                expiry_date=expiry_date,
                cvv=cvv,
                amount=amount,
                is_successful=True
            )
            payment.save()
            
            messages.success(request, 'Payment processed successfully!')
            return redirect('wallet:wallet_view')
        except Exception as e:
            messages.error(request, f'Payment failed: {str(e)}')
            return redirect('wallet:diposit')
    
    return render(request, 'wallet/diposit.html')

