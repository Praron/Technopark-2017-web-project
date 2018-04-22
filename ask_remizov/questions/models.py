# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.aggregates import Count
from random import randint


MAX_TEXT_LENGTH = 2048;
MAX_TITLE_LENGTH = 128;
MAX_TAG_LENGTH = 64;


class GetRandomObjectManager(models.Manager):
    def get_random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]


class ProfileManager(GetRandomObjectManager):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='%Y/%m/%d/', default='avatar.png')
    objects = ProfileManager()

    def __unicode__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class TagManager(GetRandomObjectManager):
    def get_popular(self, number):
        return Tag.objects.annotate(num_questions=Count('question')).order_by('-num_questions')[:number]


class Tag(models.Model):
    text = models.CharField(max_length=MAX_TAG_LENGTH)
    objects = TagManager()

    def __unicode__(self):
        return self.text


class QuestionManager(GetRandomObjectManager):
    pass


class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET(''))
    title = models.CharField(max_length=MAX_TITLE_LENGTH)
    body = models.CharField(max_length=MAX_TEXT_LENGTH)
    rating = models.IntegerField(default=0)
    publication_date = models.DateTimeField('date published', auto_now=True)
    tags = models.ManyToManyField(Tag)
    objects = QuestionManager()

    def __unicode__(self):
        return self.title


class AnswerManager(GetRandomObjectManager):
    pass


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.SET(''))
    body = models.CharField(max_length=MAX_TEXT_LENGTH)
    rating = models.IntegerField(default=0)
    objects = AnswerManager()

    def __unicode__(self):
        return self.body


class Vote(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_like =  models.BooleanField(default=True)
