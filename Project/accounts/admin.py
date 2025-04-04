from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import InvestorProfile, BusinessProfile
from django.contrib.auth.models import User 

class InvestorProfileInline(admin.StackedInline):
    model = InvestorProfile
    can_delete = False
    verbose_name_plural = 'Investor Profile'

class BusinessProfileInline(admin.StackedInline):
    model = BusinessProfile
    can_delete = False
    verbose_name_plural = 'Business Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (InvestorProfileInline, BusinessProfileInline)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(InvestorProfile)
admin.site.register(BusinessProfile)