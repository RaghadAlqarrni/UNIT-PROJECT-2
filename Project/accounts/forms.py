from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import InvestorProfile, BusinessProfile


class InvestorSignUpForm(UserCreationForm):
    SECTOR_CHOICES = [
        ('Technology', 'Technology'),
        ('Healthcare', 'Healthcare'),
        ('Finance', 'Finance'),
        ('Retail', 'Retail'),
        ('Real Estate', 'Real Estate'),
        ('Energy', 'Energy'),
        ('Entertainment', 'Entertainment'),
        ('Other', 'Other'),
    ]
    
    INCOME_SOURCE_CHOICES = [
        ('Salary', 'Salary'),
        ('Business', 'Business'),
        ('Investments', 'Investments'),
        ('Rental Income', 'Rental Income'),
        ('Pension', 'Pension'),
        ('Other', 'Other'),
    ]
    
    investment_preferences = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text='Describe your investment interests',
        required=True
    )
    portfolio_size = forms.DecimalField(
        help_text='Your current investment portfolio size',
        required=True
    )
    id_number = forms.CharField(max_length=50, required=True, help_text='Enter your ID number')
    first_name = forms.CharField(max_length=30, required=True)
    middle_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'placeholder': 'Optional'}))
    last_name = forms.CharField(max_length=30, required=True)
    income_sources = forms.ChoiceField(choices=INCOME_SOURCE_CHOICES, required=True, help_text='Select your source of income')
    employment_status = forms.ChoiceField(
        choices=[
            ('Employed', 'Employed'),
            ('Unemployed', 'Unemployed'),
            ('Self-employed', 'Self-employed'),
            ('Retired', 'Retired')
        ],
        required=True,
        help_text='Select your employment status'
    )
    monthly_income = forms.ChoiceField(
        choices=[
            ('Less than $1,000', 'Less than $1,000'),
            ('$1,000 - $5,000', '$1,000 - $5,000'),
            ('$5,000 - $10,000', '$5,000 - $10,000'),
            ('More than $10,000', 'More than $10,000'),
        ],
        required=True,
        help_text='Select your monthly income range'
    )
    beneficial_owner = forms.BooleanField(required=True, help_text='Are you the beneficial owner of this account?')
    investor_type = forms.CharField(max_length=20, required=True)
    investment_size = forms.ChoiceField(
        choices=[
            ('Small', 'Small'),
            ('Medium', 'Medium'),
            ('Large', 'Large')
        ],
        required=True
    )
    sector = forms.ChoiceField(choices=SECTOR_CHOICES, required=True, help_text='Select your sector of interest')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2', 
                  'first_name', 'middle_name', 'last_name', 
                  'id_number', 'investment_preferences', 
                  'portfolio_size', 'income_sources', 
                  'employment_status', 'monthly_income',
                  'beneficial_owner', 'investor_type', 
                  'investment_size', 'sector')


class BusinessSignUpForm(UserCreationForm):
    SECTOR_CHOICES = [
        ('Technology', 'Technology'),
        ('Healthcare', 'Healthcare'),
        ('Finance', 'Finance'),
        ('Retail', 'Retail'),
        ('Real Estate', 'Real Estate'),
        ('Energy', 'Energy'),
        ('Entertainment', 'Entertainment'),
        ('Other', 'Other'),
    ]

    project_name = forms.CharField(max_length=255, required=True, help_text='Enter project name')
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True, help_text='Provide a brief description of your project')
    funding_required = forms.DecimalField(max_digits=15, decimal_places=2, required=True, help_text='Enter the funding required for your project')
    sector = forms.ChoiceField(choices=SECTOR_CHOICES, required=True, help_text='Select the business sector')
    expected_return = forms.DecimalField(max_digits=10, decimal_places=2, required=False, help_text='Expected return on investment', widget=forms.NumberInput(attrs={'placeholder': 'Optional'}))
    