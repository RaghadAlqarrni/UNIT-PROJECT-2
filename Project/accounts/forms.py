from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import InvestorProfile, BusinessProfile


class InvestorSignUpForm(UserCreationForm):
    investment_preferences = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text='Describe your investment interests'
    )
    portfolio_size = forms.DecimalField(
        help_text='Your current investment portfolio size'
    )
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2', 
                 'first_name', 'last_name')

class BusinessSignUpForm(UserCreationForm):
    company_name = forms.CharField(max_length=255)
    company_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    industry = forms.CharField(max_length=100)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2',
                 'first_name', 'last_name')