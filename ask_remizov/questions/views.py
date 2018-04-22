# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

from django.db.models.aggregates import Count
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.csrf import csrf_protect
from questions.models import Question, Tag, Answer, Profile
from .forms import SignupForm, QuestionForm, LoginForm, AnswerForm, SettingsForm


def get_page(objects, page_size, page_number):
    paginator = Paginator(objects, page_size)
    try:
        result = paginator.page(page_number)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    return result


def get_GET_parameters(request):
    parameters = ''
    for parameter in (request.GET.items()):
        parameters += str(parameter[0] + '=' + parameter[1] + '&')
    return parameters


def get_best_members():
    return User.objects.order_by('profile__rating')[:5]


def new_questions_view(request):
    show_hot = True if int(request.GET.get('hot') or 0) else False
    questions = get_page(Question.objects.order_by('-rating' if show_hot else '-publication_date'), 3,
                         int(request.GET.get('page') or 1))
    return render(request, 'questions/base.html', {
                  'get_parameters': get_GET_parameters(request),
                  'questions': questions,
                  'best_members': get_best_members(),
                  'popular_tags': Tag.objects.get_popular(16),
                  'show_hot': show_hot,
                  })


def tag_view(request, tag_id='0'):
    tag = Tag.objects.get(pk=int(tag_id))
    questions = get_page(Question.objects.filter(tags__id=int(tag_id))
                         .order_by('-rating'), 3,
                         int(request.GET.get('page') or 1))

    return render(request, 'questions/tag.html', {
                  'tag': tag,
                  'get_parameters': get_GET_parameters(request),
                  'questions': questions,
                  'best_members': get_best_members(),
                  'popular_tags': Tag.objects.get_popular(16),
                  })


def answers_view(request, question_id='0'):
    if request.method == 'POST':
        form = AnswerForm(request.POST)        
        if form.is_valid():
            pass
            question = Question.objects.get(pk=question_id)
            body = form.cleaned_data['text']
            Answer.objects.create(author=request.user.profile, body=body,
                                  rating=0, question=question)
    else:
        form = AnswerForm()
    question = get_object_or_404(Question, pk=int(question_id))
    answers = Answer.objects.filter(question=question).order_by('-rating')
    return render(request, 'questions/answers.html', {
                  'question': question,
                  'answers': answers,
                  'best_members': get_best_members(),
                  'popular_tags': Tag.objects.get_popular(16),
                  'answer_form': form,
                  })


@csrf_protect
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['login'],
                                            first_name=form.cleaned_data['nickname'],
                                            email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password'])
            user.save()
            user.profile.avatar = form.cleaned_data['avatar']
            user.save()
            return HttpResponseRedirect('/question/')
    else:
        form = SignupForm()

    return render(request, 'questions/signup.html', {
                  'best_members': get_best_members(),
                  'popular_tags': Tag.objects.get_popular(16),
                  'signup_form': form,
                  })


@csrf_protect
@login_required
def settings_view(request):
    form = SettingsForm()
    return render(request, 'questions/settings.html', {
                  'best_members': get_best_members(),
                  'popular_tags': Tag.objects.get_popular(16),
                  'signup_form': form,
                  })


@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['login'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.GET['continue'])

    else:
        form = LoginForm()
    return render(request, 'questions/login.html', {
                  'best_members': get_best_members(),
                  'popular_tags': Tag.objects.get_popular(16),
                  'login_form': form,
                  })


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.GET['continue'])

@csrf_protect
@login_required
def ask_view(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            tags = map(lambda s: s.strip(), form.cleaned_data['tags'].split(','))
            tags = [s for s in tags if s != '']
            q = Question(author=Profile.objects.get(user=request.user),
                         title=form.cleaned_data['title'],
                         body=form.cleaned_data['text'],)
            q.save()
            for i in range(len(tags)):
                tag = Tag.objects.get_or_create(text=tags[i])[0]
                q.tags.add(tag)
            q.save()
            return HttpResponseRedirect(reverse('answers', kwargs={'question_id': str(q.id)}))
    else:
        form = QuestionForm()

    return render(request, 'questions/ask.html', {
                  'best_members': get_best_members(),
                  'popular_tags': Tag.objects.get_popular(16),
                  'ask_form': form,
                  })
