from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class InvestorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="investor_profile")
    investment_preferences = models.TextField() 
    portfolio_size = models.DecimalField(max_digits=15, decimal_places=2)  

    def __str__(self):
        return f"Investor: {self.user.username}"

class BusinessProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="business_profile")
    project_name = models.CharField(max_length=255, default="Unnamed Project")
    description = models.TextField(default="No description available.")
    funding_required = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    sector = models.CharField(max_length=255, default="General")
    expected_return = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    projected_revenue = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, default=0.00)
    created_at = models.DateTimeField(default=timezone.now)  
    updated_at = models.DateTimeField(auto_now=True) 
    def __str__(self):
        return self.project_name