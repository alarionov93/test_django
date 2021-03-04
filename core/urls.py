#

from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.index, name='site_index'),
	path('redirected', views.index, name='r_site_index'),
]