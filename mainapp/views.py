from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.


def home(request):
    return render(request,'general/home.html')

def capitalize(request):
    return render(request,'tools/capitalize.html')
