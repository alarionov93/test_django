from django.db import models
from datetime import datetime
from django.utils import timezone
from datetime import datetime, timedelta

import pytz
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ImproperlyConfigured
# from django.db.models import Q
from django.db.utils import IntegrityError

# Create your models here.

USER_TYPE_ADMIN = 1
USER_TYPE_AUTHOR = 2

class Publisher(models.Model):
	name = models.CharField(max_length=50, blank=False, null=False, unique=False)

	def __str__(self):
		return str(self.name)

	class Meta:
		db_table = 'publishers'

class InnerUserManager(BaseUserManager):
    
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('User must have an email')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.type_of = USER_TYPE_AUTHOR
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.type_of = USER_TYPE_ADMIN
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
	email = models.CharField(max_length=50, blank=False, null=False, unique=True)
	name = models.CharField(max_length=50, blank=False, null=False, unique=False)
	ex_name = models.CharField(max_length=50, blank=False, null=True, unique=True)
	type_of = models.PositiveIntegerField(default=USER_TYPE_AUTHOR, blank=False, null=False, unique=False)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)

	objects = InnerUserManager()
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	def __str__(self):
		if self.ex_name is not None:
			return "%s (known as %s)." % (self.name, self.ex_name)
		return self.name

	@property
	def full_name(self):
		return self.__str__()

	class Meta:
		db_table = 'users'
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'


class AuthorBook(models.Model):
    author = models.ForeignKey('User', to_field='id', on_delete=models.CASCADE, db_column='author_id', null=False, blank=False, unique=False)
    book = models.ForeignKey('Book', to_field='id', on_delete=models.CASCADE, db_column='book_id', null=False, blank=False, unique=False)

    def save(self, *args, **kwargs):
        if self.author.type_of != USER_TYPE_AUTHOR:
            raise ValueError("Author has wrong type_of field value!")

        return super(AuthorBook, self).save(*args, **kwargs)

    class Meta:
    	db_table = 'authors_books'


class Book(models.Model):
	name = models.CharField(max_length=200, blank=False, null=False, unique=False)
	date_of_publication = models.DateField(default=timezone.now)
	publisher = models.ForeignKey('Publisher', db_column='publisher_id', to_field='id', on_delete=models.CASCADE)
	authors = models.ManyToManyField('User', through='AuthorBook')

	def to_json(self):
		book_obj = {}
		if not self.id:
			return {}

		book_obj.update({'name': self.name})
		book_obj.update({'publisher': self.publisher})
		book_obj.update({'date_of_publication': self.date_of_publication})
		book_obj.update({'authors': [ a.__str__() for a in self.authors.all() ]})

		return book_obj

	@property
	def published_recently(self):
		return self.date_of_publication >= timezone.now() - datetime.timedelta(days=1)

	def __str__(self):
		authors = '; '.join([x.__str__() for x in self.authors.all()])
		return "Name: %s, published: %s, by %s, from %s" % (self.name, self.date_of_publication, authors, self.publisher)


	class Meta:
		db_table = 'books'


