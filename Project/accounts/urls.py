from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='sign_up'),
    path('signin/', views.sign_in, name='sign_in'),
    path('logout/', views.sign_out, name='logout'),
    path('password/change/', views.change_password, name='change_password'),

  
    path('profile/', views.profile, name='profile'),


 
    path('investor/dashboard/', views.investor_dashboard, name='investor_dashboard'),
    path('business/dashboard/', views.business_profile_view, name='business_dashboard'),

  
    path('invest/<int:project_id>/', views.invest_in_project, name='invest_in_project'),
]
