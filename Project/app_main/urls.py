from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view , name='main_view'),
    path('sign/page/', views.sign_view , name='sign_view'), 
]