from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import InvestorProfile, BusinessProfile
from django.contrib.auth.models import User 

admin.site.unregister(User)
admin.site.register(InvestorProfile)
admin.site.register(BusinessProfile)