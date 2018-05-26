from django.shortcuts import render, reverse, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from . import models
# Create your views here.


def home(request):
    return render(request,'general/home.html')

def tool(request,tool_name):
    tool = get_object_or_404(models.Tool,url_endpoint__iexact=tool_name)
    context={'tool':tool}
    return render(request,'tools/{0}'.format(tool.template_name),context)
