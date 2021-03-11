# Generated by Django 3.1.7 on 2021-03-11 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('ex_name', models.CharField(blank=True, max_length=50, null=True, unique=True)),
            ],
            options={
                'db_table': 'authors',
            },
        ),
        migrations.AlterModelTable(
            name='book',
            table='books',
        ),
        migrations.AlterModelTable(
            name='publisher',
            table='publishers',
        ),
        migrations.CreateModel(
            name='AuthorBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(db_column='author_id', on_delete=django.db.models.deletion.CASCADE, to='core.author')),
                ('book', models.ForeignKey(db_column='book_id', on_delete=django.db.models.deletion.CASCADE, to='core.book')),
            ],
            options={
                'db_table': 'authors_books',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(through='core.AuthorBook', to='core.Author'),
        ),
    ]
