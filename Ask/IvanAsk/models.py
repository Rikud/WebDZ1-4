# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class ModelManager(models.Manager):
	def sortByDate(self):
		objects_list = []
		questions = self.order_by('-date')
		for question in questions:
			list_element = self.model(id=question.id, text=question.text, title=question.title, ratin=question.ratin, tags=question.tags.all())
			list_element.answers_count = Answer.objects.filter(question_id=question.id).count()
			objects_list.append(list_element)
		return objects_list

	def bestUsers(self):
		from django.db import connection
		cursor = connection.cursor()
		cursor.execute("""
			SELECT user.nick, COUNT(*) as count 
			FROM ivanask_user user,ivanask_answer answers 
			WHERE user.id = answers.answerer_id 
			GROUP BY user.id 
			ORDER BY count DESC""")
		user_list = []
		for row in cursor.fetchall()[:5]:
			user = self.model(nick = row[0])
			user_list.append(user)
		return user_list

	def bestTags(self):
		from django.db import connection
		cursor = connection.cursor()
		cursor.execute("""
			SELECT tag.text, COUNT(*) as count 
			FROM ivanask_question_tags question_tags, ivanask_tag tag 
			WHERE tag.id = question_tags.tag_id 
			GROUP BY tag.id 
			ORDER BY count DESC""")
		tag_list = []
		for row in cursor.fetchall()[:5]:
			tag = self.model(text = row[0])
			tag_list.append(tag)
		return tag_list

	def bestQuestions(self):
		objects_list = []
		questions = self.order_by('-ratin')
		for question in questions:
			list_element = self.model(id=question.id, text=question.text, title=question.title, ratin=question.ratin, tags=question.tags.all())
			list_element.answers_count = Answer.objects.filter(question_id=question.id).count()
			objects_list.append(list_element)
		return objects_list

	def questionsByTag(self, tag):
		from django.db import connection
		cursor = connection.cursor()
		cursor.execute("""
			SELECT question_tags.question_id, tag.text
			FROM ivanask_question_tags question_tags, ivanask_tag tag 
			WHERE tag.id = question_tags.tag_id AND tag.text = '""" + tag + """'
			ORDER BY tag.id DESC""")
		objects_list = []
		for row in cursor.fetchall()[:5]:
			question = Question.objects.get(pk=row[0])
			list_element = self.model(id=question.id, text=question.text, title=question.title, ratin=question.ratin, tags=question.tags.all())
			list_element.answers_count = Answer.objects.filter(question_id=question.id).count()
			objects_list.append(list_element)
		return objects_list

	def answersOnQuestion(self, id):
		return Answer.objects.filter(question_id=id)


# Create your models here.
class User(models.Model):
	login = models.CharField(max_length=200)
	nick = models.CharField(max_length=200)
	email = models.EmailField()
	password = models.CharField(max_length=200)
	avatar = models.FileField(upload_to='uploads/')
	date = models.DateTimeField(auto_now=True)
	objects = ModelManager()

class Tag(models.Model):
	text = models.CharField(max_length=200)

class Question(models.Model):
	asking = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=200, default='')
	text = models.CharField(max_length=200)
	ratin = models.IntegerField()
	tags = models.ManyToManyField(Tag)
	date = models.DateTimeField(default=timezone.now)
	objects = ModelManager()

class Answer(models.Model):
	answerer = models.ForeignKey(User, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	text = models.CharField(max_length=200)
	correct = models.BooleanField()
	date = models.DateTimeField(default=timezone.now)
	objects = ModelManager()

class Like(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	assessment = models.SmallIntegerField();
	date = models.DateTimeField(auto_now=True)