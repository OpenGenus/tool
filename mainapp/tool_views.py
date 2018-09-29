from django.shortcuts import render, reverse, get_object_or_404,redirect
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from . import models
from PIL import Image
import base64
from css_html_js_minify import js_minify,process_single_js_file
import os
import pypandoc

import re
import json
from urllib.request import urlopen

from django.core.files.storage import default_storage
from django.conf import settings
from django.core.files.base import ContentFile, File

import urllib.request as ureq
from guesslang import Guess


import pdfkit
import sys
from django.core.files.storage import FileSystemStorage
import time
import cv2 as cv




def detect_lang(request):
    code = request.POST['code']
    lang = Guess().language_name(code)
    return HttpResponse(lang)


def website_status(request):
    if request.method == "POST":
        url = request.POST.get('in')
        try:
            page = ureq.urlopen(url)
            status = page.getcode()
            if status != 200:
                return HttpResponse('<p>Website is offline</p>')
            else:
                return HttpResponse('<p>Website is online</p>')
        except:
            return HttpResponse('<p>Website does not exist</p>')

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

def convert_image(request):
    if request.method=='POST':
        image_to_convert = request.FILES.get('image')
        convert_to = request.POST.get('convert_to')

        filename, ext = os.path.splitext(image_to_convert.name)
        outputfile_name = '{0}.{1}'.format(filename, convert_to)
        input_file_path = os.path.join(settings.MEDIA_ROOT, 'cartoonify/input', image_to_convert.name)
        output_file_path = os.path.join(settings.MEDIA_ROOT, 'cartoonify/output', outputfile_name)
        path = default_storage.save(input_file_path, ContentFile(image_to_convert.read()))

        inpImage = cv.imread(input_file_path,1)
        inpImage2 = inpImage
        imgBilFilter = cv.bilateralFilter(inpImage2, 9,9,7)
        imgGray = cv.cvtColor(imgBilFilter, cv.COLOR_RGB2GRAY)
        imgfilter = cv.medianBlur(imgGray, 5)
        imgEdge = cv.adaptiveThreshold(imgfilter, 255, cv.ADAPTIVE_THRESH_MEAN_C,
                                            cv.THRESH_BINARY, 9, 2);
        imgColored = cv.cvtColor(imgEdge, cv.COLOR_GRAY2RGB)
        imgFinal = cv.bitwise_and(inpImage, imgColored)
        cv.imwrite(settings.MEDIA_ROOT+"/cartoonify/output/convertedImg.png", imgFinal)
        return render(request,'tools/image_tools/cartoonify_output.html', {'input_file': input_file_path, 
           'output_file': settings.MEDIA_ROOT+"/cartoonify/output/convertedImg.png"})
        
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




def generate_pdf(request):
    
    weburl=request.POST["webpageurl"]
    config = pdfkit.configuration(wkhtmltopdf=settings.BASE_DIR+'/wkhtmltopdf/bin/wkhtmltopdf.exe')
    pdfkit.from_url(weburl, settings.MEDIA_ROOT+'\generatedpdf\generatedpdf.pdf',configuration=config)
    return render(request,'tools/pdf_generator/result_page.html',{'file_path':settings.MEDIA_ROOT+'\generatedpdf\generatedpdf.pdf'})
            
   
    

def  delete_generated_pdf(request,path):
    
    if os.path.isfile(path):
        os.remove(path)
    
    return HttpResponse('file deleted')
    
    
    
def download_generated_pdf(request,path):
    file_path = path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'attachment; filename='+ file_path
            return response
    raise HttpResponse('file Not Found')
    
    
    
def view_generated_pdf(request,path):
    file_path = path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename='+ file_path
            return response
    raise HttpResponse('file Not Found')        
 
    
