# Generated by Django 5.0 on 2024-01-05 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0005_alter_authors_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authors',
            name='date_of_birth',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='authors',
            name='date_of_death',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
    ]
