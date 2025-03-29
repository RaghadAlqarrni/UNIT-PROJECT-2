from django.urls import path
from . import views



app_name = "app_business"

urlpatterns = [
    path('business/detail/', views.business_detail_view , name='business_detail_view'),
   
]