#

from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.index, name='site_index'),
	path('login/', views.login, name='site_login'),
	path('books/', views.books, name='site_books'),
	path('logout/', views.logout, name='site_logout'),
	path('register/', views.register, name='site_register'),
]