import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from . import models
from . import forms
from django.contrib.auth import authenticate, login as sign_in, logout as sign_out
from django.contrib.auth.decorators import login_required
# Create your views here.


def register(request):
	if request.method == 'POST':
		form = forms.RegistrationForm(request.POST)
		if form.is_valid():
			user = models.User.objects.create(
			  name=form.cleaned_data['name'],
			  password=form.cleaned_data['password1'],
			  email=form.cleaned_data['email'],
			)
			user.save()

		return redirect(to=reverse('site_login'))
	else:
		form = forms.RegistrationForm()
	return render(request, 'register.html', context={'form': form})


def login(request):
	ctx = {}
	if request.method == 'POST':
		email = request.POST.get('email', None)
		passwd = request.POST.get('password', None)
		if email and passwd:
			user = authenticate(request, username=email, password=passwd)
		else:
			ctx.update({'error':'Форма содержит пустые поля.'})
		# import pdb
		# pdb.set_trace()
		if user is not None and user.is_active:
			sign_in(request, user)
			return redirect(to=reverse('site_index'), args=('asdfg', 123))
		else:
			ctx.update({'error':'Пользователь не активен или неверные учётные данные.'})
	return render(request, template_name='login.html', context=ctx)


def logout(request):
	sign_out(request)
	path = request.GET.get('path', None)
	if path is None:
		path = '/'
	return redirect(to=path)


def index(request, reg_success=None):
  # import pdb
  # pdb.set_trace()
	ctx = {}

	return render(request, template_name='index.html', context=ctx)


@login_required(login_url='/login/')
def books(request):
	ctx = {}
	ctx.update({ 'books': [ b.to_json() for b in models.Book.objects.all() ] })

	return render(request, template_name='books.html', context=ctx)