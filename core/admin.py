from django.contrib import admin

from . import models
# Register your models here.

admin.site.register(models.Publisher)
admin.site.register(models.AuthorBook)
admin.site.register(models.Book)
admin.site.register(models.User)