# Generated by Django 5.0 on 2024-01-05 22:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0002_rename_country_authors_country_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='authors',
            old_name='country_id',
            new_name='country',
        ),
    ]