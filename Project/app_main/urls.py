from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = "app_main"

urlpatterns = [
    path('', views.main_view , name='main_view'),
    path('sign/page/', views.sign_view , name='sign_view'), 
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("request-otp/", views.request_otp, name="request_otp"),
    path("invester/detail/", views.invester_view, name="invester_view"),
    path("login/page/", views.login_view, name="login_view"),
    path("business/signup/", views.business_signup, name="business_signup"),
    
]