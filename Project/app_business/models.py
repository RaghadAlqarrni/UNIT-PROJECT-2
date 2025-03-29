from django.db import models
from django.contrib.auth import get_user_model

class Project(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="projects")
    project_name = models.CharField(max_length=255)
    description = models.TextField()
    sector = models.CharField(max_length=100, choices=[
        ('Technology', 'Technology'),
        ('Real Estate', 'Real Estate'),
        ('Retail', 'Retail'),
        ('Manufacturing', 'Manufacturing'),
        ('Other', 'Other'),
    ])
    funding_required = models.DecimalField(max_digits=15, decimal_places=2)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    founders = models.TextField(blank=True, null=True)  # List of founders
    registration_number = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    revenue_model = models.TextField(blank=True, null=True)
    expected_return = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    projected_revenue = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    business_plan = models.FileField(upload_to="business_plans/", blank=True, null=True)
    project_image = models.ImageField(upload_to="project_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.project_name
