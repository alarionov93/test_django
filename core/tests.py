
from datetime import datetime
from django.test import TestCase
from django.utils import timezone
from . import models

# Create your tests here.

class BookTest(TestCase):
	
	# test method should begin with 'test_%s'!
	def test_if_book_date_is_in_future(self):
		date_time = timezone.now() + datetime.timedelta(days=30)
		future_book = models.Book(date_of_publication=date_time.date())
		self.assertIs(future_book.published_recently, False)

