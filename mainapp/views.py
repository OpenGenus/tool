
from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from django.shortcuts import render, reverse, get_object_or_404
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
    user_profile = models.UserProfile.objects.get(user__username=user_name)
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
