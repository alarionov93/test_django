from django.shortcuts import render, get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.response import Response
from core import models
from .serializers import BookSerializer
# Create your views here.

# TODO: Serialize BookStar relation!

class BookList(generics.ListAPIView):
	model = models.Book
	serializer_class = BookSerializer

	def get_queryset(self, *args, **kwargs):
		qs = models.Book.objects.all()
		return qs


class BookListViewSet(viewsets.ViewSet):

	def list(self, request):
		queryset = models.Book.objects.all()
		serializer = BookSerializer(queryset, many=True)
		return Response(serializer.data)

	def retrieve(self, request, pk=None):
		queryset = models.Book.objects.all()
		book = get_object_or_404(queryset, pk=pk)
		serializer = BookSerializer(book)
		return Response(serializer.data)

	def create(self, validated_data):
        # items_data = validated_data.po

        # similar to Parent.objects.create(**validated_data)
		return super().create(**validated_data)

        # for item_data in items_data:
            # Item.objects.create(parent=parent, **item_data)
        # return parent
