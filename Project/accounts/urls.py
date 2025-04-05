from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='sign_up'),
    path('signup/investor/', views.investor_signup, name='investor_sign_up'),
    path('signup/business/', views.business_signup, name='business_sign_up'),
    path('profile/<user_name>/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('password/change/', views.change_password, name='change_password'),
    path('signin/', views.sign_in, name='sign_in'),
    path('logout/', views.sign_out, name='logout'),
]