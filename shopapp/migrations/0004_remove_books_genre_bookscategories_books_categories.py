# Generated by Django 5.0 on 2024-01-05 15:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0003_alter_category_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='books',
            name='genre',
        ),
        migrations.CreateModel(
            name='BooksCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopapp.books')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopapp.category')),
            ],
        ),
        migrations.AddField(
            model_name='books',
            name='categories',
            field=models.ManyToManyField(blank=True, through='shopapp.BooksCategories', to='shopapp.category'),
        ),
    ]