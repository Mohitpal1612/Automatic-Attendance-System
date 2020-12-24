from django.shortcuts import render
from django.http import HttpResponse
#create your views here

def  dashboard(request):
    return render(request,"dashboard.html")    