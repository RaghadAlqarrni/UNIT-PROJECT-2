from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signin/', views.sign_in, name='sign_in'),
    path('signup/investor/', views.investor_signup, name='investor_sign_up'),
    path('signup/business/', views.business_signup, name='business_sign_up'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('password/change/', views.change_password, name='change_password'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
]