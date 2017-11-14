# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from pprint import pformat
from cgi import parse_qsl, escape
from loremipsum import get_sentence
from loremipsum import get_paragraph
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from IvanAsk.models import User, Question, Answer, Like, Tag
import random 
import re

# Create your views here.

def paginate(objects_list, request):
	paginator = Paginator(objects_list, 5)
	page = request.GET.get('page')
	try:
		questions = paginator.page(page)
	except PageNotAnInteger:
		questions = paginator.page(1)
	except EmptyPage:
		questions = paginator.page(paginator.num_pages)
	return questions

def index(request):
	objects_list = Question.objects.sortByDate()
	topUsers = User.objects.bestUsers()
	topTags = Question.objects.bestTags()
	questions = paginate(objects_list, request)
	context = {'questions' : questions, 'title' : 'Ask Ivan', 'topUsers' : topUsers, 'topTags': topTags}
	return(render(request,"index.html", context))
	#return HttpResponse(request)

def login(request):
	question = "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Rem aliquam minima esse molestiae hic ullam deserunt laboriosam non voluptate adipisci quia ipsam incidunt voluptatem excepturi ab, harum porro ea. Placeat, nemo sint! Aliquid eligendi repudiandae natus, maxime officiis libero, veniam ipsum sunt fuga sapiente, consequatur ut aliquam aperiam molestias hic."
	context = {'question' : question, 'title' : 'Ask Ivan'}
	return(render(request,"login.html", context))

def signup(request):
	question = "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Rem aliquam minima esse molestiae hic ullam deserunt laboriosam non voluptate adipisci quia ipsam incidunt voluptatem excepturi ab, harum porro ea. Placeat, nemo sint! Aliquid eligendi repudiandae natus, maxime officiis libero, veniam ipsum sunt fuga sapiente, consequatur ut aliquam aperiam molestias hic."
	context = {'question' : question, 'title' : 'Ask Ivan'}
	return(render(request,"signup.html", context))

def ask(request):
	question = "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Rem aliquam minima esse molestiae hic ullam deserunt laboriosam non voluptate adipisci quia ipsam incidunt voluptatem excepturi ab, harum porro ea. Placeat, nemo sint! Aliquid eligendi repudiandae natus, maxime officiis libero, veniam ipsum sunt fuga sapiente, consequatur ut aliquam aperiam molestias hic."
	context = {'question' : question, 'title' : 'Ask Ivan'}
	return(render(request,"new-question.html", context))

def presonal_page(request):
	question = "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Rem aliquam minima esse molestiae hic ullam deserunt laboriosam non voluptate adipisci quia ipsam incidunt voluptatem excepturi ab, harum porro ea. Placeat, nemo sint! Aliquid eligendi repudiandae natus, maxime officiis libero, veniam ipsum sunt fuga sapiente, consequatur ut aliquam aperiam molestias hic."
	context = {'question' : question, 'title' : 'Ask Ivan'}
	return(render(request,"presonal_page.html", context))

def question(request, qid):
	result = re.search(r'(\d)+', request.path_info)
	if result != None:
		id = result.group(0)
	else:
		id = str(1)
	topUsers = User.objects.bestUsers()
	topTags = Question.objects.bestTags()
	question = Question.objects.get(pk=id)
	answers = Answer.objects.answersOnQuestion(id)
	context = {'answers' : answers, 'title' : 'Ask Ivan', 'question' : question, 'topUsers' : topUsers, 'topTags': topTags}
	return(render(request,"question.html", context))
	
def searchByTag(request):
	tag = request.GET.get('tag')
	objects_list = Question.objects.questionsByTag(tag)
	topUsers = User.objects.bestUsers()
	topTags = Question.objects.bestTags()
	questions = paginate(objects_list, request)
	context = {'questions' : questions, 'title' : 'Ask Ivan', 'topUsers' : topUsers, 'topTags': topTags, 'searchTag':tag}
	return(render(request,"listByTag.html", context))

def hot(request):
	objects_list = Question.objects.bestQuestions()
	topUsers = User.objects.bestUsers()
	topTags = Question.objects.bestTags()
	questions = paginate(objects_list, request)
	context = {'questions' : questions, 'title' : 'Ask Ivan', 'topUsers' : topUsers, 'topTags': topTags}
	return(render(request,"hot.html", context))

def getPostParameters(request):
	output = ['<p>WSGI!</p>']
	output.append('Hello world!')
	output.append('<br>')
	output.append('Post:')
	output.append('<form method="post" ')
	output.append('action="http://localhost/getPostParameters">')
	output.append('<input type="text" name = "test">')
	output.append('<input type="submit" value="Send">')
	output.append('</form>')
	if request.META['SERVER_PORT'] == '8080':
		if request.META['REQUEST_METHOD'] == 'POST':
			output.append('<h1>Post data:</h1>')
			for key, val in request.POST.iteritems():
				output.append(key + ' = ' + val)
				output.append('<br>')
		if request.GET:
			output.append('<h1>Get data:</h1>')
			for key in request.GET.keys():
				val = request.GET.get_list(key)
			#for key, val in request.GET.iteritems()::
				output.append(key + ' = ' + val)
				output.append('<br>')
		output.append(request.POST)
	return HttpResponse(output)