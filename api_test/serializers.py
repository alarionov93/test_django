
from core import models
from rest_framework import serializers


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    # legal_name = serializers.CharField(read_only=True, required=False)

    # def get_fields(self):
        # fields = super(UserSerializer, self).get_fields()
        # 
        # return fields
    # @property
    # def user_type(self):
    # 	if self.model.type_of == models.USER_TYPE_AUTHOR:
    # 		user_type = 'author'
    # 	elif self.model.is_admin == True:
    # 		user_type = 'admin'
    # 	else:
    # 		user_type = 'user'
    # 	return user_type

    queryset = models.User.objects.filter(type_of=models.USER_TYPE_AUTHOR)

    class Meta:
        model = models.User
        # TODO: iterate ALL needed user fields
        fields = ('id', 'full_name', 'email', 'type_of')


class PublisherSerializer(serializers.HyperlinkedModelSerializer):
	# queryset = models.Publisher.objects.all()

	class Meta:
		model = models.Publisher
		# TODO: iterate ALL needed user fields
		fields = ('id', 'name')

# class StarredBookSerializer(BookSerializer):

# 	class Meta:
# 		model = models.Book
# 		fields = ('id', 'date_of_publication', 'name',)


class BookSerializer(serializers.HyperlinkedModelSerializer):
	authors = AuthorSerializer(many=True)
	publisher = PublisherSerializer(many=False)

	class Meta:
		model = models.Book
		fields = ('id', 'date_of_publication', 'name', 'starred', 'authors', 'publisher')

