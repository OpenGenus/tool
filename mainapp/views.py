
from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from django.shortcuts import render, reverse, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse, FileResponse
from . import models, tool_views
from PIL import Image

from fpdf import FPDF
import os

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
	print(tool.template_name,"   template   ",sep="    ")
	print('tools/{0}/{1}'.format(category,tool.template_name))
	if ( request.method == 'POST' and tool_name == "resume_builder" ):
		pdf = FPDF()
		pdf.add_page()
		pdf.set_auto_page_break(auto= bool, margin = 5)
		name = request.POST.get('asliname')
		pdf.set_top_margin(margin = 5)
		pdf.set_font('Arial', 'B', 35)
		pdf.multi_cell(w=0,h=13,txt=name.strip().rstrip("\n\r"),align='C')
		address = request.POST.get('address')
		email = request.POST.get('email')		
		phone = request.POST.get('phone')
		about = request.POST.get('about')
		pdf.set_font('Times','', 16)
		pdf.multi_cell(w=0,h=8,txt=address.strip().rstrip("\n\r"),align='C')
		pdf.multi_cell(w=0,h=8,txt=email.strip().rstrip("\n\r"),align='C')
		pdf.multi_cell(w=0,h=8,txt=phone.strip().rstrip("\n\r"),align='C')
		pdf.multi_cell(w=0,h=10,txt=about.strip().rstrip("\n\r"),align='C')
		
		#pdf.line(5,55,205,55)
		pdf.multi_cell(w=0,h=9,txt=" ",align='C')

		#All Correctly Retrieving
		pdf.set_font('Arial', 'B', 20)
		pdf.multi_cell(w=0,h=10,txt="Profile",align='L')	
		profile = request.POST.get('totalprofile')	
		profile = int(profile) #Total
		pro1 = request.POST.get('temp')
		pdf.set_font('Times','', 15)
		#if ( type(pro1) == 'str' ):
		pdf.multi_cell(w=0,h=7,txt=pro1.strip().rstrip("\n\r"),align='L')
		#print(pro1," PROFILE ",sep="  ")
		lineheight = 81
		for i in range(1,profile):
			temp = "temp"+str(i)
			rest = request.POST.get(temp)
			pdf.multi_cell(w=0,h=7,txt=rest.strip().rstrip("\n\r"),align='L')
			lineheight = lineheight+7
			#print(rest," PROFILE ",sep="  ")

		#pdf.line(5,lineheight,205,lineheight)		
		pdf.multi_cell(w=0,h=9,txt=" ",align='C')

		#All Correctly Retrieving
		pdf.set_font('Arial', 'B', 20)
		pdf.multi_cell(w=0,h=10,txt="Work Experience",align='L')
		work = request.POST.get('totalwork')
		work = int(work) #Total
		com1 = request.POST.get("companyplate2")
		pos1 = request.POST.get("positionplate2")
		dur1 = request.POST.get("durationplate2")
		wor1 = request.POST.get("workdoneplate2")
		#if ( type(com1) == 'str' ):
		pdf.set_font('Times','B', 15)
		pdf.multi_cell(w=0,h=7,txt=com1.strip().rstrip("\n\r"),align='L')
		pdf.set_font('Times','B', 15)
		pdf.multi_cell(w=0,h=7,txt=pos1.strip().rstrip("\n\r"),align='L')
		pdf.set_font('Times','', 15)
		pdf.multi_cell(w=0,h=7,txt=dur1.strip().rstrip("\n\r"),align='L')
		pdf.multi_cell(w=0,h=7,txt=wor1.strip().rstrip("\n\r"),align='L')
		#print(com1,pos1,dur1,wor1,sep="   ")
		lineheight = lineheight + 47
		pdf.multi_cell(w=0,h=3,txt=" ",align='C')
		for i in range(1,work):
			comp = "companyplate2"+str(i)
			rest1 = request.POST.get(comp)
			pos = "positionplate2"+str(i)
			rest2 = request.POST.get(pos)
			dur = "durationplate2"+str(i)
			rest3 = request.POST.get(dur)
			wor = "workdoneplate2"+str(i)
			rest4 = request.POST.get(wor)
			pdf.set_font('Times','B', 15)
			pdf.multi_cell(w=0,h=7,txt=rest1.strip().rstrip("\n\r"),align='L')
			lineheight = lineheight+7
			pdf.set_font('Times','B', 15)
			pdf.multi_cell(w=0,h=7,txt=rest2.strip().rstrip("\n\r"),align='L')
			lineheight = lineheight+7
			pdf.set_font('Times','', 15)
			pdf.multi_cell(w=0,h=7,txt=rest3.strip().rstrip("\n\r"),align='L')
			lineheight = lineheight+7
			pdf.multi_cell(w=0,h=7,txt=rest4.strip().rstrip("\n\r"),align='L')
			lineheight = lineheight+7
			pdf.multi_cell(w=0,h=3,txt=" ",align='C')
			#print(rest1,rest2,rest3,rest4,sep="   ")

		#pdf.line(5,lineheight,205,lineheight)		
		pdf.multi_cell(w=0,h=9,txt=" ",align='C')

		#All Correctly Retrieving
		pdf.set_font('Arial', 'B', 20)
		pdf.multi_cell(w=0,h=10,txt="Education",align='L')
		edu = request.POST.get('totaledu')
		edu = int(edu) #Total
		ini1 = request.POST.get("institutiontemplate3")
		score1 = request.POST.get("scoretemplate3")
		edudur1 = request.POST.get("duration2template3")
		#if ( type(ini1) == 'str' ):
		pdf.set_font('Times','B', 15)
		pdf.multi_cell(w=0,h=7,txt=ini1.strip().rstrip("\n\r"),align='L')
		pdf.set_font('Times','B', 15)
		pdf.multi_cell(w=0,h=7,txt=edudur1.strip().rstrip("\n\r"),align='L')
		pdf.set_font('Times','', 15)
		pdf.multi_cell(w=0,h=7,txt=score1.strip().rstrip("\n\r"),align='L')
		#print(ini1,score1,edudur1,sep="   ")
		lineheight = lineheight + 40
		pdf.multi_cell(w=0,h=3,txt=" ",align='C')
		for i in range(1,edu):
			ini = "institutiontemplate3"+str(i)
			rest1 = request.POST.get(ini)
			score = "scoretemplate3"+str(i)
			rest2 = request.POST.get(score)
			edudur = "duration2template3"+str(i)
			rest3 = request.POST.get(edudur)
			pdf.set_font('Times','B', 15)
			pdf.multi_cell(w=0,h=7,txt=rest1.strip().rstrip("\n\r"),align='L')
			lineheight = lineheight+7
			pdf.set_font('Times','B', 15)
			pdf.multi_cell(w=0,h=7,txt=rest3.strip().rstrip("\n\r"),align='L')
			lineheight = lineheight+7
			pdf.set_font('Times','', 15)
			pdf.multi_cell(w=0,h=7,txt=rest2.strip().rstrip("\n\r"),align='L')
			lineheight = lineheight+7
			pdf.multi_cell(w=0,h=3,txt=" ",align='C')
			#print(rest1,rest2,rest3,sep="   ")

		#pdf.line(5,lineheight,205,lineheight)		
		pdf.multi_cell(w=0,h=9,txt=" ",align='C')

		#All Correctly Retrieving
		pdf.set_font('Arial', 'B', 20)
		pdf.multi_cell(w=0,h=10,txt="Projects",align='L')
		proj = request.POST.get('totalproj')
		proj = int(proj) #Total
		project1 = request.POST.get("projectlate2")
		tech1 = request.POST.get("techlate2")
		projdur1 = request.POST.get("projectdurationlate2")
		projwor1 = request.POST.get("projectdonelate2")		
		#if ( proj >= 1 ):
		pdf.set_font('Times','B', 15)
		pdf.multi_cell(w=0,h=7,txt=project1.strip().rstrip("\n\r"),align='L')
		pdf.set_font('Times','B', 15)
		pdf.multi_cell(w=0,h=7,txt=tech1.strip().rstrip("\n\r"),align='L')
		pdf.set_font('Times','', 15)
		pdf.multi_cell(w=0,h=7,txt=projdur1.strip().rstrip("\n\r"),align='L')
		pdf.multi_cell(w=0,h=7,txt=projwor1.strip().rstrip("\n\r"),align='L')
		lineheight = lineheight + 47
		pdf.multi_cell(w=0,h=3,txt=" ",align='C')
		#print(project1,tech1,projdur1,projwor1,sep="   ")
		for i in range(1,proj):
			project = "projectlate2"+str(i)
			rest1 = request.POST.get(project)
			tech = "techlate2"+str(i)
			rest2 = request.POST.get(tech)
			projdur = "projectdurationlate2"+str(i)
			rest3 = request.POST.get(projdur)
			projwor = "projectdonelate2"+str(i)
			rest4 = request.POST.get(projwor)
			pdf.set_font('Times','B', 15)
			pdf.multi_cell(w=0,h=7,txt=rest1.strip().rstrip("\n\r"),align='L')
			lineheight = lineheight+7
			pdf.set_font('Times','B', 15)
			pdf.multi_cell(w=0,h=7,txt=rest2.strip().rstrip("\n\r"),align='L')
			lineheight = lineheight+7
			pdf.set_font('Times','', 15)
			pdf.multi_cell(w=0,h=7,txt=rest3.strip().rstrip("\n\r"),align='L')
			lineheight = lineheight+7
			pdf.multi_cell(w=0,h=7,txt=rest4.strip().rstrip("\n\r"),align='L')
			lineheight = lineheight+7
			pdf.multi_cell(w=0,h=3,txt=" ",align='C')
			#print(rest1,rest2,rest3,rest4,sep="   ")

		#pdf.line(5,lineheight,205,lineheight)		
		pdf.multi_cell(w=0,h=9,txt=" ",align='C')

		#All Correctly Retrieving
		pdf.set_font('Arial', 'B', 20)
		pdf.multi_cell(w=0,h=10,txt="Skills",align='L')
		skill = request.POST.get('totalskill')
		skill = int(skill) #Total
		skill1 = request.POST.get("skillkill")
		diffi1 = request.POST.get("kill")
		print(skill)
		if ( diffi1 == 'Intermediate' or diffi1 == 'Advance' or diffi1 == 'Beginner' ):
			pdf.set_font('Times','B', 15)
			pdf.multi_cell(w=0,h=7,txt=skill1.strip().rstrip("\n\r"),align='L')
			pdf.set_font('Times','', 15)
			pdf.multi_cell(w=0,h=7,txt=diffi1.strip().rstrip("\n\r"),align='L')
		lineheight = lineheight + 33
		pdf.multi_cell(w=0,h=3,txt=" ",align='C')
		#print(skill1,diffi1,sep="   ")
		for i in range(1,skill):
			skill = "skillkill"+str(i)
			rest1 = request.POST.get(skill)
			diffi = "kill"+str(i)
			rest2 = request.POST.get(diffi)
			pdf.set_font('Times','B', 15)
			pdf.multi_cell(w=0,h=7,txt=rest1.strip().rstrip("\n\r"),align='L')
			lineheight = lineheight+7
			pdf.set_font('Times','', 15)
			pdf.multi_cell(w=0,h=7,txt=rest2.strip().rstrip("\n\r"),align='L')
			lineheight = lineheight+7
			pdf.multi_cell(w=0,h=3,txt=" ",align='C')
			#print(rest1,rest2,sep="   ")

		#pdf.line(5,lineheight,205,lineheight)		
		pdf.multi_cell(w=0,h=9,txt=" ",align='C')
		
		#All Correctly Retrieving
		pdf.set_font('Arial', 'B', 20)
		pdf.multi_cell(w=0,h=10,txt="Awards",align='L')
		award = request.POST.get('totalaward')
		award = int(award) #Total
		achieve1 = request.POST.get("achievementward")
		awarddone1 = request.POST.get("awarddoneward")
		#if ( type(achieve1) == 'str' ):
		pdf.set_font('Times','B', 15)
		pdf.multi_cell(w=0,h=7,txt=achieve1.strip().rstrip("\n\r"),align='L')
		pdf.set_font('Times','', 15)
		pdf.multi_cell(w=0,h=7,txt=awarddone1.strip().rstrip("\n\r"),align='L')
		lineheight = lineheight + 33
		pdf.multi_cell(w=0,h=3,txt=" ",align='C')
		#print(achieve1,awarddone1,sep="   ")
		for i in range(1,award):
			achieve = "achievementward"+str(i)
			rest1 = request.POST.get(achieve)
			awarddone = "awarddoneward"+str(i)
			rest2 = request.POST.get(awarddone)
			pdf.set_font('Times','B', 15)
			pdf.multi_cell(w=0,h=7,txt=rest1.strip().rstrip("\n\r"),align='L')
			lineheight = lineheight+7
			pdf.set_font('Times','', 15)
			pdf.multi_cell(w=0,h=7,txt=rest2.strip().rstrip("\n\r"),align='L')
			lineheight = lineheight+7
			pdf.multi_cell(w=0,h=3,txt=" ",align='C')
			#print(rest1,rest2,sep="   ")

		#pdf.line(5,lineheight,205,lineheight)		
		pdf.multi_cell(w=0,h=9,txt=" ",align='C')

		#All Correctly Retrieving
		pdf.set_font('Arial', 'B', 20)
		pdf.multi_cell(w=0,h=10,txt="Interests",align='L')
		inter = request.POST.get('totalinter')
		inter = int(inter) #Total
		interest1 = request.POST.get("inter")
		pdf.set_font('Times','', 15)
		#if ( type(interest1) == 'str' ):
		pdf.multi_cell(w=0,h=7,txt=interest1.strip().rstrip("\n\r"),align='L')
		lineheight = lineheight + 26
		pdf.multi_cell(w=0,h=3,txt=" ",align='C')
		#print(interest1,sep="   ")
		for i in range(1,inter):
			interest = "rest"+str(i)
			rest1 = request.POST.get(interest)
			pdf.multi_cell(w=0,h=7,txt=rest1.strip().rstrip("\n\r"),align='L')
			lineheight = lineheight+7
			pdf.multi_cell(w=0,h=3,txt=" ",align='C')
			#print(rest1,sep="   ")
		
		dirspot = os.getcwd()
		print(dirspot+" DIRECTORY DEKHO ")
		pdf.output(dirspot+'/resume.pdf', 'F')
		filename=dirspot+'/resume.pdf'
		#return FileResponse(as_attachment=True, filename=dirspot+'/resume.pdf')
		return FileResponse(open(filename, 'rb'), content_type='application/pdf')
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
