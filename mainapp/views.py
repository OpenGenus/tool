
from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from . import models, tool_views
from PIL import Image

from sumy.parsers.plaintext import PlaintextParser
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.edmundson import EdmundsonSummarizer as Summarizer0
from sumy.summarizers.lsa import LsaSummarizer as Summarizer1
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer2
from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer3
from sumy.summarizers.luhn import LuhnSummarizer as Summarizer4
from sumy.summarizers.sum_basic import SumBasicSummarizer as Summarizer5
from sumy.summarizers.kl import KLSummarizer as Summarizer6
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
import random
import base64
import hmac
import hashlib
import  pickle
import urllib
from urllib import parse
import binascii


from hashlib import sha256
import hmac
from base64 import b64decode, b64encode



def discourse_login(request):
    

    generated_nonce=generate_nonce()
    
    request.session['auth_nonce']=generated_nonce
    
    data = { 'nonce': generated_nonce, 'return_sso_url':settings.DISCOURSE_LOGIN_REDIRECT_URL } 

    payload = urllib.parse.urlencode(data)
    
    payload = b64encode(payload.encode())
    
    sig = hmac.new(settings.DISCOURSE_SSO_SECRET.encode(), payload, sha256).hexdigest()
    query_string = parse.urlencode({'sso': payload, 'sig': sig})
    
    return HttpResponseRedirect('%s?%s' % (settings.DISCOURSE_ROOT_URL, query_string)) 
    
        
             
      
        

@login_required(login_url='/discourse_login/')
def discourse_login_success(request):   
    
    payload = request.GET.get('sso')
    sig = request.GET.get('sig')
        
    if(validate_sig(payload, sig)):
        if 'auth_nonce' in request.session:
            nonce = request.session['auth_nonce']
            if(get_nonce(payload)==nonce):        
                request.session['user_login']=True        
                return home(request)
        
        
    
     
    
 



def logout (request):
   
    request.session['user_login']=False
    return redirect('/')



def generate_nonce(length=8):
    
    return ''.join([str(random.randint(0, 9)) for i in range(length)])







def home(request):
    
    tools = models.Tool.objects.all()
    categories = models.Tool.objects.order_by().values_list('category',flat=True).distinct()
    context={'tools':tools,'categories':categories}
    print(settings.MEDIA_URL)
    return render(request,'general/home.html',context)


def validate_sig(payload,sig):
    
    payload = urllib.parse.unquote(payload)
    computed_sig = hmac.new(settings.DISCOURSE_SSO_SECRET.encode(), payload.encode(),sha256).hexdigest()
    return hmac.compare_digest(computed_sig,sig)
       
        
def get_nonce( payload):
    payload = b64decode(urllib.parse.unquote(payload)).decode()
    d = dict(nonce.split("=") for nonce in payload.split('&'))

    if 'nonce' in d and d['nonce'] != '':
        return d['nonce']
    else:
        
        raise Exception("Nonce could not be found in payload")
    



def tool(request,tool_name):
	tool = get_object_or_404(models.Tool,url_endpoint__iexact=tool_name)
	context={'tool':tool}
	category = tool.category.replace(" ", "_").lower()
	print('tools/{0}/{1}'.format(category,tool.template_name))
	if ( request.method == "POST" and tool_name == "text_summary" ):
		print("   POST DEKHO ",tool_name,sep="  ")
		inp = request.POST.get('input')
		aslinp = inp
		lang = request.POST.get('Languages')
		algo = request.POST.get('Algorithm')
		percen = request.POST.get('percentage')
		parser = PlaintextParser.from_string(inp, Tokenizer(lang))
		stemmer = Stemmer(lang)
		if ( algo == "Edmundson" ):
			summarizer = Summarizer0(stemmer)
			summarizer.stop_words = get_stop_words(lang)
		elif ( algo == "Latent Semantic Analysis" ):
			summarizer = Summarizer1(stemmer)
			summarizer.stop_words = get_stop_words(lang)
		elif ( algo == "LexRank" ):
			summarizer = Summarizer2(stemmer)
			summarizer.stop_words = get_stop_words(lang)
		elif ( algo == "TextRank" ):
			summarizer = Summarizer3(stemmer)
			summarizer.stop_words = get_stop_words(lang)		
		elif ( algo == "Luhn" ):
			summarizer = Summarizer4(stemmer)
			summarizer.stop_words = get_stop_words(lang)
		elif ( algo == "SumBasic" ):
			summarizer = Summarizer5(stemmer)
			summarizer.stop_words = get_stop_words(lang)
		elif ( algo == "KL-Sum" ):
			summarizer = Summarizer6(stemmer)
			summarizer.stop_words = get_stop_words(lang)
		summary = []
		for sentence in summarizer(parser.document, percen):
			summary.append(sentence)
		result = ''.join(str(v) for v in summary)
		print(result)
		context={ 'tool':tool,'summary': result, 'asliinp':aslinp }
		return render(request,'tools/text_tools/text_summary.html',context)
	else:
		return render(request,'tools/{0}/{1}'.format(category,tool.template_name),context)

def user_profile(request,user_name):
    user_profile = get_object_or_404(models.UserProfile,user__username=user_name)
    tools = user_profile.author_tool_set.all()
    return render(request,'user/profile.html',{'user_profile':user_profile,'tools':tools})

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



    
    

