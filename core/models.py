from django.db import models

# Create your models here.
class Publisher(models.Model):
  name = models.CharField(max_length=30, null=False,\
      blank=False, unique=False, verbose_name="Имя")
  address = models.CharField(max_length=50, null=True,\
      blank=True, unique=False, db_column="addr", verbose_name="Адрес")


  class Meta:
    db_table = 'publishers'


class Book(models.Model):
  """docstring for Book"""
  name = models.CharField(max_length=100, null=False, blank=False, unique=False)
  publisher = models.ForeignKey('Publisher', to_field='id',\
      db_column='publisher_id', on_delete=models.CASCADE, blank=True,\
      null=True, unique=False, verbose_name='Издатель')

  def __str__(self):
    return "%s" % name

  class Meta:
    db_table = 'books'
    