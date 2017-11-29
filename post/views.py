# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
import urllib2
import urllib
import json
import os

from django.shortcuts import render
from .models import Post
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.contrib import auth
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.context_processors import csrf
from django.core.paginator import Paginator
from .forms import PostForm, PostInstagramForm
# Create your views here.


def main(request, page_number=1):
	print('MAIN')
	context = {}
	username = request.user.username
	# user_like_list = []
	posts_list = Post.objects.all().order_by('-post_date')
	# for post in posts_list:
	# 	if username in post.return_list_of_user():
	# 		user_like_list.append(post.id)
	current_page = Paginator(posts_list, 2)
	if username:
		context['username'] = username		
	context['list_of_posts'] = current_page.page(page_number)
	# context['user_like_list'] = user_like_list
	return render(request, 'post/main.html', context)


def signup(request):
    if request.method == 'POST':
    	print('request.POST : ', request.POST)
        form = SignupForm(request.POST)
        print('form : ', form)
        print('form.is_valid() : ', form.is_valid())
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('post/acc_active_email.html', {
                'user':user, 
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your blog account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    
    else:
        form = SignupForm()
    
    return render(request, 'post/signup.html', {'form': form})


def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		login(request, user)
		# return redirect('home')
		# return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
		return redirect('/')
	else:
		return HttpResponse('Activation link is invalid!')


def login_func(request):
	args = {}
	args.update(csrf(request))
	if request.POST:
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request, user)
			return redirect('/')
		else:
			args['login_error'] = 'Log in error'
			return render_to_response('post/login.html', args)
	else:
		return render(request, 'post/login.html', args)


def logout(request):
    auth.logout(request)
    return redirect('/')


def post_image_page(request):
	context = {}
	username = request.user.username
	context.update(csrf(request))
	context['username'] = username
	if request.method == 'POST':
		print('It is POST method!###############################################')
		# args.update(csrf(request))
		print('request.POST : ', request.POST)
		print('request.POST : ', request.FILES)
		form = PostForm(request.POST, request.FILES)
		print('form: ', form)
		print('form.is_valid(): ', form.is_valid())
		if form.is_valid():
			print('Form is valid!#################################################')
			post = form.save(commit=False)
			post.save()
			return redirect('/')
		else:
			print('ELSE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
			context['form'] = form
			return render(request, 'post/post_image_page.html', context)
	else:
		context['form'] = PostForm()
		return render(request, 'post/post_image_page.html', context)


def ajaxRequest(url=None):
	"""
	Makes an ajax get request.
	url - endpoint(string)
	"""
	req = urllib2.Request(url)
	f = urllib2.urlopen(req)
	response = f.read()
	f.close()
	return response	

def find_between( s, first, last ):
	print("Func working!")
	# print('type(instagramJSON) : ', type(instagramJSON))
	print('s.index( first ) = ', s.decode('utf-8').index( first ))
	try:
		print('TRY!')
		start = s.decode('utf-8').index( first ) + len( first )
		print('start : ', start)
		end = s.decode('utf-8').rindex( last, start )
		print('end : ', end)
		return s.decode('utf-8')[start:end]
	except ValueError:
		return "error!"


def find_description(s, first, last):
	print("Func working!")
	try:
		start = s.decode('utf-8').index( first ) + len( first )
		print start
		print(last)
		print('!!!!!!!!!!!!!!!!!!!')
		# print(s[start::].split(last)[0])
		print('!!!!!!!!!!!!!!!!!!!')
		print(s.decode('utf-8')[start::].decode('utf-8').split(last)[0])
		print(len(s.decode('utf-8')[start::].decode('utf-8').split(last)[0]))
		end = len(s.decode('utf-8')[start::].decode('utf-8').split(last)[0]) + start
		print end
		return s.decode('utf-8')[start:end]
	except ValueError:
		return "error!"


def post_inst_image_page(request):
	context = {}
	username = request.user.username
	context.update(csrf(request))
	context['username'] = username
	if request.method == 'POST':
		print('It is POST method!###############################################')
		# args.update(csrf(request))
		print('request.POST : ', request.POST)
		print('request.FILES : ', request.FILES)
		form = PostInstagramForm(request.POST)
		print('form :', form.is_valid())
		print('##################################################################################form: ', form)
		# print('form.is_valid(): ', form.is_valid())
		print('form :', form)
		image_url = form.cleaned_data['post_image_url']
		post_title = form.cleaned_data['post_title']
		print('image_url : ', image_url)

		##################################################################################

		access_token = "2225471298.1677ed0.f0414147ed34435499dd57df48c2b217"
		print("access_token : ", access_token)
		# ask for hashtag name
		# hashtag = "book"

		# url to query for pictures
		# nextUrl = "https://www.instagram.com/p/BcAkWypFbak/?taken-by=9gag/?access_token="+access_token
		nextUrl = image_url+'/?access_token='+access_token
		print ('nextUrl : ', nextUrl)
		# while there is a next url to go to
		if nextUrl:
			# request the data at that endpoint 
			instagramJSON = ajaxRequest(nextUrl)

		print(find_between( instagramJSON, 'display_url": "', '", "display_resources' ))
		imageUrl = find_between( instagramJSON, 'display_url": "', '", "display_resources' )
		# print(find_between( instagramJSON, '{"edges": [{"node": {"text": "', "\n" ))
		print(find_between( instagramJSON, '• ', " UTC" ))
		date_of_post = find_between( instagramJSON, '• ', " UTC" )
		print("DATE OF POST!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", date_of_post)
		date_of_post = datetime.strptime(date_of_post, "%b %d, %Y at %I:%M%p")
		print("DATE OF POST!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", date_of_post)

		print('Date_of_post : ', date_of_post)
		description_of_post = find_description(instagramJSON, '{"edges": [{"node": {"text": "', '"}}]}')
		description_of_post = description_of_post.encode('utf-8')
		print('description_of_post : ', description_of_post)
		description_of_post = " ".join(description_of_post.split('\\n'))
		print('description_of_post : ', description_of_post)
		print("TYPE OF description_of_post", type(description_of_post))
		print('description_of_post : ', description_of_post)

		time = str(datetime.now())
		print('data : ', date_of_post)
		fullfilename = os.path.join('static/', time+".jpg")
		# urllib.urlretrieve(url, fullfilename)
		image = urllib.urlretrieve(imageUrl, fullfilename)
		print('form :', form)
		print('image', image)
		post = Post.objects.create(post_image_url=imageUrl, post_image=image[0], post_title=post_title, post_date=date_of_post, post_description=description_of_post)
		print('post : ', post)
		# post.post_image = image
		# post.post_title = time+".jpg"
		# post.post_date = datetime.now()
		# post.post_description = description_of_post
		# post.save()
		print('form :', form)
		print('form.is_valid() :', form.is_valid())
		print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
		####################################################################################
		return redirect('/')
		# if form.is_valid():
		# 	print('Form is valid!#################################################')
		# 	post = form.save(commit=False)
		# 	post.save()
		# 	return redirect('/')
		# else:
		# 	print('ELSE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
		# 	context['form'] = form
		# 	return render(request, 'post/post_inst_image_page.html', context)
	else:
		context['form'] = PostInstagramForm()
		return render(request, 'post/post_inst_image_page.html', context)