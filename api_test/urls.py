from django.urls import path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'books', views.BookListViewSet, basename='book')
urlpatterns = router.urls

# urlpatterns = [
	# path('books/', views.BookList.as_view(), name='api_book_list'),
# ]