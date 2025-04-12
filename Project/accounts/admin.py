from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.contrib.auth.models import User 

from .models import InvestorProfile

admin.site.register(Investment)
admin.site.register(Notification)
admin.site.register(InvestorProfile)


