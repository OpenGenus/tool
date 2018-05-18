from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.


def home(request):
    return render(request,'general/home.html')

def tool(request,tool_name):
    # json processing
    return render(request,'tools/{0}.html'.format(tool_name))
