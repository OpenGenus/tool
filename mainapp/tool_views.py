
from django.shortcuts import render, reverse, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from . import models
from PIL import Image
import base64
from css_html_js_minify import js_minify,process_single_js_file
import os
import pypandoc
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.files.base import ContentFile

import urllib.request as ureq

def website_status(request):
    if request.method == "POST":
        url = request.POST.get('in')
        try:
            page = ureq.urlopen(url)
            status = page.getcode()
            if status != 200:
                return HttpResponse(url+" is offline")
            else:
                return HttpResponse(url+" is online")
        except:
            return HttpResponse(url+" does not exist")

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


def jpg_to_png(request):
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




def show_minified_js(request):
    if request.method == "POST":
        z = js_minify(request.POST.get('code'))
        return JsonResponse({"code":z})
    return HttpResponse('<script>alert("error")</script>')

def download_file(request):
    if request.method == "POST":
        z = js_minify(request.POST.get('code'))
        res = HttpResponse(str(z),content_type="application/js")
        res['Content-Disposition'] = 'attachment; filename=yourname.js'
        return res
    return HttpResponse('<script>alert("error")</script>')

def download_minified_file(request):
    if request.method == "POST":
        input_file_path = os.path.join(settings.MEDIA_ROOT,'files',request.FILES.get("file").name)
        path = default_storage.save(input_file_path,ContentFile(request.FILES.get("file").read()))
        z = process_single_js_file(input_file_path,overwrite=False)
        print(z);
        with open(z, 'rb+') as fh:
            res = HttpResponse(fh.read(),content_type="application/js")
            res['Content-Disposition'] = 'attachment; filename='+ os.path.basename(z)
            return res
    return HttpResponse('<script>alert("error")</script>')


def about_sample_file(request,format):
    name = "sample."+format
    print("i am working for ",name)
    input_file_path = os.path.join(settings.MEDIA_ROOT,'sample',name)
    with open(input_file_path, 'rb+') as fh:
        size = os.path.getsize(input_file_path)/1024
        if(size<2000):
            size = round(size,2)
            size = str(size) + " KB"
        else:
            size = round(size/1024,2)
            size = str(size)+" MB"
    return JsonResponse({"name":name,"size":size})

def download_sample_file(request,format):
    name = "sample."+format
    input_file_path = os.path.join(settings.MEDIA_ROOT,'sample',name)
    with open(input_file_path, 'rb+') as fh:
        response = HttpResponse(fh.read(), content_type="application/"+format)
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(input_file_path)
        return response
    return HttpResponse('Error while converting', status=404)
