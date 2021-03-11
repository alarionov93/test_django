from django.db import models
from datetime import datetime
from django.utils import timezone

# Create your models here.


class Publisher(models.Model):
	name = models.CharField(max_length=50, blank=False, null=False, unique=False)

	def __str__(self):
		return str(self.name)

	class Meta:
		db_table = 'publishers'


class Author(models.Model):
	name = models.CharField(max_length=50, blank=False, null=False, unique=False)
	ex_name = models.CharField(max_length=50, blank=False, null=True, unique=True)

	def __str__(self):
		if self.ex_name is not None:
			return "%s (known as %s)." % (self.name, self.ex_name)
		return self.name

	class Meta:
		db_table = 'authors'


class AuthorBook(models.Model):
    author = models.ForeignKey('Author', to_field='id', on_delete=models.CASCADE, db_column='author_id', null=False, blank=False, unique=False)
    book = models.ForeignKey('Book', to_field='id', on_delete=models.CASCADE, db_column='book_id', null=False, blank=False, unique=False)

    class Meta:
    	db_table = 'authors_books'


class Book(models.Model):
	name = models.CharField(max_length=200, blank=False, null=False, unique=False)
	date_of_publication = models.DateField(default=timezone.now)
	publisher = models.ForeignKey('Publisher', db_column='publisher_id', to_field='id', on_delete=models.CASCADE)
	authors = models.ManyToManyField('Author', through='AuthorBook')

	def to_json(self):
		pass

	@property
	def published_recently(self):
		return self.date_of_publication >= timezone.now() - datetime.timedelta(days=1)

	def __str__(self):
		authors = '; '.join([x.__str__() for x in self.authors.all()])
		return "Name: %s, published: %s, by %s, from %s" % (self.name, self.date_of_publication, authors, self.publisher)

	# def save(self):
	# 	#
	# 	return super(Book, self).save(*args, **kwargs)

	class Meta:
		db_table = 'books'


