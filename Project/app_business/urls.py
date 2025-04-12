from django.urls import path
from . import views



app_name = "app_business"

urlpatterns = [
    path('detail/', views.projects_view, name='business_detail_view'),
    path('project/<int:project_id>/', views.business_detail_view, name='project_opp'),
      
]