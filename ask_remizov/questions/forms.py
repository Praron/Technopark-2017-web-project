from django import forms
from django.contrib.auth.models import User
from questions.models import Question, Tag, Answer, Profile
from django.contrib.auth import login, authenticate, logout
from re import match

class SignupForm(forms.Form):
    login = forms.CharField(label='Login', min_length=4, max_length=128)
    email = forms.EmailField(label='Email', min_length=5, max_length=128)
    nickname = forms.CharField(label='Nickname', min_length=4, max_length=34)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', min_length=5, max_length=128)
    password_again = forms.CharField(widget=forms.PasswordInput, label='Password again', min_length=5, max_length=128)
    avatar = forms.ImageField(required=False)

    def clean_login(self):
        login = self.cleaned_data['login']
        if User.objects.filter(username=login).exists():
            raise forms.ValidationError("Login already exists")
        return login

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        if User.objects.filter(first_name=nickname).exists():
            raise forms.ValidationError("Nickname already exists")
        return nickname

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean(self):
        form_data = self.cleaned_data
        if form_data['password'] != form_data['password_again']:
            raise forms.ValidationError("Passwords do not match")
        return form_data

# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = ['title', 'body', 'tags']
#         widgets = {
#             'title': forms.TextInput(
#                 attrs={'class': 'col-xs-40 submit form-control', 'placeholder': 'Enter your question here'}
#             ),
#             'body': forms.Textarea(
#                 attrs={'class': 'col-xs-40 submit form-control', 'cols': 80, 'rows': 20,
#                        'placeholder': 'Enter the more detailed version of the question'}
#             ),
#         }

class QuestionForm(forms.Form):
    title = forms.CharField(label='Title', min_length=5, max_length=128)
    text = forms.CharField(label='Text', widget=forms.Textarea(), min_length=8, max_length=2048)
    tags = forms.CharField(label='Tags', required=False, min_length=0, max_length=128)

    def clean_tags(self):
        cleaned_tags = self.cleaned_data['tags']
        if match('^[a-zA-Z0-9_ ,]*$', cleaned_tags) is None:
            raise forms.ValidationError('Tags may only contain letters, numbers, spaces,'
                                        + ' underscores aand separated by comma')
        return cleaned_tags


class LoginForm(forms.Form):
    login = forms.CharField(label='Login', min_length=3, max_length=128)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', min_length=5, max_length=128)

    def clean(self):
        login = self.cleaned_data['login']
        password = self.cleaned_data['password']
        if not authenticate(username=login, password=password):
            raise forms.ValidationError('Incorrect login and/or password')
        return self.cleaned_data


class AnswerForm(forms.Form):
    text = forms.CharField(label='Text', widget=forms.Textarea(), min_length=4, max_length=2048)


class SettingsForm(forms.Form):
    email = forms.EmailField(label='Email', required=False, min_length=5, max_length=128)
    nickname = forms.CharField(label='Nickname', required=False, min_length=4, max_length=34)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', min_length=5, max_length=128)
    password_again = forms.CharField(widget=forms.PasswordInput, label='Password again', min_length=5, max_length=128)
    avatar = forms.ImageField(required=False)

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        if User.objects.filter(first_name=nickname).exists():
            raise forms.ValidationError("Nickname already exists")
        return nickname

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean(self):
        form_data = self.cleaned_data
        if form_data['password'] != form_data['password_again']:
            raise forms.ValidationError("Passwords do not match")
        return form_data