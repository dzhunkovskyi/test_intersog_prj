from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.admin import widgets
from .models import Post
from datetime import datetime


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    birthday = forms.DateField(initial='month/day/year')
    country = forms.CharField()
    city = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'birthday',
        		  'country', 'city')


class PostForm(forms.ModelForm):
	post_title = forms.CharField(max_length=200)
	post_description = forms.CharField(max_length=200)
	post_date = forms.DateTimeField(initial=datetime.now())
	post_image = forms.ImageField()

	class Meta:
		model = Post
		fields = ['post_title', 'post_description', 'post_date', 'post_image']


class PostInstagramForm(forms.ModelForm):
	post_title = forms.CharField(max_length=200)
	# post_description = forms.CharField(max_length=200, widget=forms.HiddenInput())
	# post_date = forms.DateTimeField(initial=datetime.now(), widget=forms.HiddenInput())
	post_image_url = forms.CharField(initial='<empty>', max_length=400)
	# post_image = forms.ImageField(initial=None, widget=forms.HiddenInput())

	class Meta:
		model = Post
		# fields = ['post_title', 'post_description', 'post_date', 'post_image_url']
		fields = ['post_title', 'post_image_url']
