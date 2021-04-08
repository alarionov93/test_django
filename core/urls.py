#

from django.urls import path, include
from . import views
from django.conf.urls.static import static
from test_django import dev_settings

urlpatterns = [
	path('', views.index, name='site_index'),
	path('login/', views.login, name='site_login'),
	path('books/', views.books, name='site_books'),
	path('books/recent/', views.RecentBooks.as_view(), name='site_recent_books'),
	path('logout/', views.logout, name='site_logout'),
	path('register/', views.register, name='site_register'),
	path('books/<int:book_id>/star/', views.StarBook.as_view(), name='star_book'),
	path('certs/', views.certificate, name='сertificate'),
] + static(dev_settings.STATIC_URL, document_root=dev_settings.STATIC_URL)