from django.db import models
from django.contrib.auth.models import User

class InvestorProfile(models.Model):
    SECTOR_CHOICES = [
        ('Technology', 'Technology'),
        ('Healthcare', 'Healthcare'),
        ('Finance', 'Finance'),
        ('Real Estate', 'Real Estate'),
        ('Education', 'Education'),
        ('Energy', 'Energy'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_number = models.CharField(max_length=50, unique=True, default="000000")
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30)
    investment_preferences = models.TextField(blank=True)
    portfolio_size = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    income_sources = models.CharField(max_length=50, blank=True)
    employment_status = models.CharField(max_length=20, blank=True)
    monthly_income = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    beneficial_owner = models.BooleanField(default=False)
    investor_type = models.CharField(max_length=20, default="Individual")
    investment_size = models.CharField(max_length=10, default="Small")
    sector = models.CharField(max_length=20, choices=SECTOR_CHOICES, default='Other')

    def __str__(self):
        return f"{self.user.username} - Investor"


class BusinessProfile(models.Model):
    SECTOR_CHOICES = [
        ('Technology', 'Technology'),
        ('Retail', 'Retail'),
        ('Manufacturing', 'Manufacturing'),
        ('Healthcare', 'Healthcare'),
        ('Finance', 'Finance'),
        ('Education', 'Education'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    founder_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100)
    business_location = models.CharField(max_length=255)
    start_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    sector = models.CharField(max_length=20, choices=SECTOR_CHOICES)
    funding_required = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    equity_offered = models.FloatField(default=0.0)
    expected_roi = models.FloatField(default=0.0)
    revenue_model = models.CharField(max_length=255, blank=True)
    projected_revenue = models.TextField(blank=True)
    business_plan = models.FileField(upload_to='business_plans/', null=True, blank=True)
    project_image = models.ImageField(upload_to='project_images/', null=True, blank=True)
    registration_document = models.FileField(upload_to='registration_docs/', null=True, blank=True)
    pitch_deck = models.FileField(upload_to='pitch_decks/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - Business"
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Profile {self.user.username}"
   