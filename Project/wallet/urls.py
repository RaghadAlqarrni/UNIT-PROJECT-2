from django.urls import path
from . import views

app_name = 'wallet'

urlpatterns = [
    path('wallet/', views.wallet_view , name='wallet_view'), 
    path('diposit/', views.diposit , name='diposit'), 
   

]