from django.shortcuts import render, reverse, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect, Http404
from . import models
from PIL import Image
import base64
# Create your views here.


def home(request):
    tools = models.Tool.objects.all()
    categories = models.Tool.objects.order_by().values_list('category',flat=True).distinct()
    context={'tools':tools,'categories':categories}
    return render(request,'general/home.html',context)

def tool(request,tool_name):
    tool = get_object_or_404(models.Tool,url_endpoint__iexact=tool_name)
    context={'tool':tool}
    print(tool.tags.all())
    return render(request,'tools/{0}'.format(tool.template_name),context)

def user_profile(request,user_name):

    user_profile = get_object_or_404(models.UserProfile,user__username=user_name)
    tools = user_profile.author_tool_set.all()
    return render(request,'user/profile.html',
                                        {'user_profile':user_profile,'tools':tools})

def tags(request,tag_name):
    tag = get_object_or_404(models.Tag,tag=tag_name)
    tools = tag.tool_set.all()
    print(tools)
    return render(request,'general/tags.html',{'tools':tools})


def category(request,category_name):
    tools = models.Tool.objects.filter(category__iexact=category_name)
    context= {'category':category,'tools':tools}
    return render(request,'general/category.html',context)

import os
import pypandoc
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.files.base import ContentFile


def convert_file(request):
    if request.method=="POST":
        file_to_convert = request.FILES.get('file')
        convert_to = request.POST.get('convert_to')

        filename, ext = os.path.splitext(file_to_convert.name)
        outputfile_name = '{0}.{1}'.format(filename,convert_to)
        input_file_path = os.path.join(settings.MEDIA_ROOT,'files',file_to_convert.name)
        output_file_path= os.path.join(settings.MEDIA_ROOT,'files',outputfile_name)
        path = default_storage.save(input_file_path,ContentFile(file_to_convert.read()))

        output = pypandoc.convert_file(input_file_path,convert_to,outputfile=output_file_path)

        if os.path.exists(output_file_path):
            print('exists')
            with open(output_file_path, 'rb+') as fh:
                response = HttpResponse(fh.read(), content_type="application/force-download")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(output_file_path)
                return response

        return HttpResponse('Error while converting', status=404)


def JpgToPng(request):
    if request.method=="POST":
        file_to_convert = request.FILES.get('file')
        convert_to = request.POST.get('convert_to')

        filename, ext = os.path.splitext(file_to_convert.name)
        outputfile_name = '{0}.{1}'.format(filename,convert_to)
        input_file_path = os.path.join(settings.MEDIA_ROOT,'files',file_to_convert.name)
        output_file_path= os.path.join(settings.MEDIA_ROOT,'files',outputfile_name)
        path = default_storage.save(input_file_path,ContentFile(file_to_convert.read()))
        im = Image.open(input_file_path)
        im.save(output_file_path)
        png_img = Image.open(output_file_path)
        print("saved file: ", png_img) 

        if os.path.exists(output_file_path):
            print('exists')
            with open(output_file_path, 'rb+') as fh:
                response = HttpResponse(fh.read(), content_type="application/force-download")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(output_file_path)
                return response

        return HttpResponse('Error while converting', status=404)