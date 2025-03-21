from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view , name='main_view'),
    path('sign/page/', views.sign_view , name='sign_view'), 
    path("verify-otp/", views.verify_otp_view, name="verify_otp"),
    path("resend-otp/", views.resend_otp, name="resend_otp"),
]