from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class InvestorProfile(models.Model):
    EMPLOYMENT_STATUS = [
        ('employed', 'Employed'),
        ('self_employed', 'Self-Employed'),
        ('unemployed', 'Unemployed'),
        ('student', 'Student'),
        ('retired', 'Retired'),
    ]

    INVESTMENT_TYPES = [
        ('equity', 'Equity'),
        ('loan', 'Loan-Based'),
        ('revenue', 'Revenue Sharing'),
        ('donation', 'Donation-Based'),
    ]

    INVESTMENT_DURATION_CHOICES = [
        ('short', 'Short Term (≤ 1 year)'),
        ('mid', 'Medium Term (1-3 years)'),
        ('long', 'Long Term (3+ years)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', default='default-avatar.png')
    roi = models.FloatField(default=0.0)
    level = models.CharField(max_length=100, default='Newbie')
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS, default='unemployed')
    preferred_investment_type = models.CharField(max_length=20, choices=INVESTMENT_TYPES, default='equity')
    investment_duration = models.CharField(max_length=10, choices=INVESTMENT_DURATION_CHOICES, default='mid')
    industries_of_interest = models.TextField(blank=True)
    investment_size = models.CharField(max_length=100, blank=True)

    def projects_count(self):
        return self.investment_set.count()

    def __str__(self):
        return self.user.username


class BusinessProfile(models.Model):
    SECTOR_CHOICES = [
        ('Tech', 'Technology'),
        ('Edu', 'Education'),
        ('Fin', 'Finance'),
        ('Med', 'Healthcare'),
        ('Agr', 'Agriculture'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('pending', 'Pending Review'),
        ('funded', 'Funded'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    founder_name = models.CharField(max_length=255, null=True, blank=True)
    registration_number = models.CharField(max_length=100, null=True, blank=True)
    business_location = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(default=timezone.now)
    description = models.TextField()
    sector = models.CharField(max_length=20, choices=SECTOR_CHOICES, default='Other')
    revenue_model = models.CharField(max_length=255, null=True, blank=True)
    projected_revenue = models.TextField(null=True, blank=True)
    business_plan = models.FileField(upload_to='media/business_plans/', null=True, blank=True)
    project_image = models.ImageField(upload_to='media/project_images/', default="default.jpg")
    registration_document = models.FileField(upload_to='media/registration_documents/', null=True, blank=True)
    pitch_deck = models.FileField(upload_to='media/pitch_decks/', null=True, blank=True)
    funding_required = models.DecimalField(max_digits=15, decimal_places=2)
    amount_raised = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    equity_offered = models.FloatField(default=0.0)
    expected_roi = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def funding_percentage(self):
        return round((self.amount_raised / self.funding_required) * 100, 2) if self.funding_required else 0

    def __str__(self):
        return self.project_name

    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Profile {self.user.username}"
    

class Investment(models.Model):
    investor = models.ForeignKey(InvestorProfile, on_delete=models.CASCADE)
    project = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE)  # أو Project إذا كنت تستخدم Model مستقل
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.investor.user.username} invested {self.amount} in {self.project.project_name}"
    


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    message = models.CharField(max_length=255)                
    timestamp = models.DateTimeField(auto_now_add=True)       
    read = models.BooleanField(default=False)                 
    def __str__(self):
        return f"{self.user.username}: {self.message[:50]}"



   