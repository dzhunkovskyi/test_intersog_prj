# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
        form = SignupForm(request.POST)
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
	if request.method == 'POST':
		pass
	else:
		context = {}
		username = request.user.username
		context['username'] = username
		return render(request, 'post/post_image_page.html', context)