from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Payment
from django.contrib import messages

# Create your views here.



def wallet_view(request):
    return render(request, 'wallet/wallet.html')


@login_required
def diposit(request):
    if request.method == 'POST':
        card_number = request.POST.get('card-number')
        card_name = request.POST.get('card-name')
        expiry_date = request.POST.get('expiry-date')
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
            return redirect('wallet:wallet')
        except Exception as e:
            messages.error(request, f'Payment failed: {str(e)}')
            return redirect('wallet:diposit')
    
    return render(request, 'wallet/diposit.html')

