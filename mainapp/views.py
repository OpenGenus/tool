from django.shortcuts import render, reverse, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from . import models
from PIL import Image

# Create your views here.
def home(request):
    tools = models.Tool.objects.all()
    categories = models.Tool.objects.order_by().values_list('category',flat=True).distinct()
    context={'tools':tools,'categories':categories}
    print(settings.MEDIA_URL)
    return render(request,'general/home.html',context)

def tool(request,tool_name):
    tool = get_object_or_404(models.Tool,url_endpoint__iexact=tool_name)
    context={'tool':tool}
    category = tool.category.replace(" ", "_").lower()
    return render(request,'tools/{0}/{1}'.format(category,tool.template_name),context)

def user_profile(request,user_name):
    user_profile = get_object_or_404(models.UserProfile,user__username=user_name)
    tools = user_profile.author_tool_set.all()
    return render(request,'user/profile.html',
                                        {'user_profile':user_profile,'tools':tools})

def timeline(request):
    tools = models.Tool.objects.all().order_by('-created_at')
    return render(request,'general/timeline.html',{'tools':tools})


def tags(request,tag_name):
    tag = get_object_or_404(models.Tag,tag=tag_name)
    tools = tag.tool_set.all()
    print(tools)
    return render(request,'general/tags.html',{'tools':tools})


def category(request,category_name):
    tools = models.Tool.objects.filter(category__iexact=category_name)
    context= {'category':category,'tools':tools}
    return render(request,'general/category.html',context)
