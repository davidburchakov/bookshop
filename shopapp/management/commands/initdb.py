from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Initialize the database'

    def handle(self, *args, **options):
        self.stdout.write('Executing SQL script to initialize the database...')
        file_path = 'shopapp/db/init.sql'  # Update this to the correct path

        with open(file_path, 'r') as file:
            sql_script = file.read()

        with connection.cursor() as cursor:
            cursor.execute(sql_script)

        self.stdout.write(self.style.SUCCESS('Database initialized successfully!'))
