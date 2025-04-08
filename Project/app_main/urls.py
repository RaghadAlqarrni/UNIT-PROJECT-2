from django.urls import path
from . import views

app_name = "app_main"

urlpatterns = [
    path('', views.main_view , name='main_view'),
    path("invester/detail/", views.invester_view, name="invester_view"),
    path('contect/page/', views.contact , name='contact'),
    path('about/page/', views.about_view , name='about_view'),
    
]