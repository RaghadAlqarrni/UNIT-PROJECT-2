from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from accounts.models import BusinessProfile
# Create your views here.

def projects_view(request):
    projects = BusinessProfile.objects.all()
    return render(request, 'app_business/business_detail.html', {'projects': projects})




def business_detail_view(request, project_id):
    project = get_object_or_404(BusinessProfile, id=project_id)
    return render(request, 'app_business/business_opp.html', {'project': project})













