# Generated by Django 3.1.7 on 2021-03-25 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_bookstar'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bookstar',
            unique_together={('book_id', 'user_id')},
        ),
    ]