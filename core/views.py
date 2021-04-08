import json
import traceback
import hashlib
import xlrd
import base64
import urllib

from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse

from . import models
from . import forms
from .mixins import JSONResponseMixin
from django.contrib.auth import authenticate, login as sign_in, logout as sign_out
from django.contrib.auth.decorators import login_required
from django.views.generic import View, CreateView, UpdateView, ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured, MultipleObjectsReturned
from django.db.utils import IntegrityError
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


def calc_uuid(fio, phone):
	# hashlib.sha256().update().hexdigest() # UID
	# import pdb
	# pdb.set_trace()
	res = [x for x in str(base64.b64encode(b'%s^%s' 
		% (
			bytes(str(fio), encoding='utf-8'),
			bytes(str(phone), encoding='utf-8')
		)
	))]
	return ''.join(res[2:len(res)-1])


def get_names(file):
	# Table:
	# |         0          |           1          |
	# |        FIO         |     +79660123456     |
	try:
		idx = 0
		names = []
		wb = xlrd.open_workbook(file_contents=file.file.read(), on_demand = True)
		wb_first_sheet = wb.sheet_by_index(idx)
		for r in range(wb_first_sheet.nrows):
			fio = wb_first_sheet.cell_value(r,0) # FIO
			phone = wb_first_sheet.cell_value(r,1) # Phone
			names.append({
				'fio': fio,
				'phone': phone
			})

		return names
	except FileNotFoundError as e:
		print("File not found!")
	except IndexError as e:
		print("Can not get sheet with specified index %s" % idx)
	except TypeError as e:
		print("File contents of %s has wrong type" % file)
		print(traceback.format_exception(None, e, e.__traceback__))
	except Exception as e:
	# except AttributeError!!
		print(traceback.format_exception(None, e, e.__traceback__))
	finally:
		if 'wb' in locals():
			wb.release_resources()
			del wb


def index(request):
	ctx = {}
  	
	if request.method == 'POST':
  		# upload file and render list with links
  		# filename = request.FILES
		# print(request.FILES)
		# import pdb
		# pdb.set_trace()
		# for name_data in names:
			# calc_uuid(name_data['fio'], name_data['phone'])
		try:
			ctx.update({'cert_links': 
				[{'link': 'certs/?id=%s' % calc_uuid(x['fio'], x['phone']), 'name': x['fio']} for x in get_names(request.FILES.get('children_data', None))]
				})
		except xlrd.biffh.XLRDError:
			ctx = {'error': "File must be XLS!"}
		# for idx, file in request.FILES.items():
			# names = get_names(file)
	else:
		# ctx.update({'cert_links': []})
		pass

	return render(request, template_name='index.html', context=ctx)


@login_required(login_url='/login/')
def books(request):
	ctx = {}
	ctx.update({ 'books': [ b.to_json() for b in models.Book.objects.all() ] })

	return render(request, template_name='books.html', context=ctx)

def certificate(request):
	ctx = {}
	cert_encoded = None
	try:
		cert_encoded = request.get_full_path().split('id=')[1]
	except IndexError:
		print("Missing id of cert!")
	if cert_encoded is not None:
		# import pdb
		# pdb.set_trace()
		# res = [x for x in str(base64.b64decode(bytes(cert_encoded, encoding='utf-8')))]
		ctx.update({'cert_id': cert_encoded})
		ctx.update({'cert_name': base64.b64decode(cert_encoded).decode('utf-8').split("^")[0]})
		ctx.update({'cert_phone': base64.b64decode(cert_encoded).decode('utf-8').split("^")[1]})

	return render(request, template_name='certificate.html', context=ctx)

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class RecentBooks(ListView):
    context_object_name = 'books'
    template_name = 'books.html'
    queryset = [obj for obj in models.Book.objects.all() if obj.published_recently is True]


# user, book
# TODO: implement method decorator as a auth mixin
# @method_decorator(, na)
class StarBook(CreateView, JSONResponseMixin):

	model = models.BookStar
	fields = ['book', 'user']
	book = None

	# request handling, parsing url params, etc.
	def dispatch(self, request, *args, **kwargs):
		print('dispatch') # print method name to show invoking order
		# print(request.GET)
		book_id = kwargs.get('book_id', None)
		if book_id is not None:
			self.book = get_object_or_404(
	            models.Book,
	            id=book_id
	        )

		return super(StarBook, self).dispatch(request)

	# prepare data for context to be passed to response
	def get_context_data(self, **kwargs):
		print('get_context_data')
		ctx = super(StarBook, self).get_context_data()

		return ctx

	# process GET request
	def get(self, request, *args, **kwargs):
		print('get')
		# here 
		if not self.request.is_ajax(): # deprecated since 3.1 !
			return HttpResponse(json.dumps({"Error": "Should be ajax"}), status=405)

		return super(StarBook, self).get(request)

	# process POST and PUT request
	def post(self, request, *args, **kwargs):
		print('post')
		super(StarBook, self).post(request)
		user_id = self.request.POST.get('user_id', None)
		ctx = {}
		try:
			# user = self.request.user
			user = models.User.objects.get(pk=user_id)
			if self.book and user:
				try:
					self.object = models.BookStar.objects.create(book=self.book, user=user)
				except IntegrityError as e:

					print("Book Star is already persists in DB!")
					ctx.update({'not_created_reason': 'already persists in db'})
				# print(self.book)
				# print(user)
				ctx.update({'created_with_id': self.object.id})
			else:
				raise ValueError("Book or user is None!")
		except models.User.DoesNotExist:
			print("User with specified id not found")
		except Exception as e:
			print(traceback.format_exception(None, e, e.__traceback__))

		return HttpResponse(json.dumps(ctx), content_type='application/json')


