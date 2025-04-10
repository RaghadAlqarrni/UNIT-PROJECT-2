from django.urls import path
from . import views



app_name = "app_business"

urlpatterns = [
    path('detail/', views.business_detail_view , name='business_detail_view'),
    path('business/signup/', views.business_signup_view , name='business_signup_view'),
   
]