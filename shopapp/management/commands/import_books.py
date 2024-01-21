from django.core.management.base import BaseCommand
import pandas as pd
import ast
from django.utils.text import slugify

from ...models.models import Books, Authors, Category, BooksCategories

class Command(BaseCommand):
    help = 'Import books from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csvfile', type=str, help='The CSV file to import.')

    def handle(self, *args, **options):
        # Get the path to the CSV file
        csv_file_path = options['csvfile']

        # Read the CSV file with pandas
        df = pd.read_csv(csv_file_path, nrows=7000)
        df.dropna(subset=['Title', 'description', 'authors', 'image', 'previewLink', 'categories'], inplace=True)

        for index, row in df.iterrows():
            # Handle authors
            try:
                author_names = ast.literal_eval(row['authors'])  # Safely evaluate the string
            except (ValueError, SyntaxError):
                author_names = []

            author_objects = []
            for name in author_names:
                author, created = Authors.objects.get_or_create(fullname=name.strip())
                author_objects.append(author)

            # Handle categories
            try:
                category_names = ast.literal_eval(row['categories'])  # Safely evaluate the string
            except (ValueError, SyntaxError):
                category_names = []

            category_objects = []
            for name in category_names:
                category, created = Category.objects.get_or_create(name=name.strip())
                category_objects.append(category)

            title = row['Title'][:255]
            img = row['image']

            # Create the book instance without authors
            book = Books.objects.create(
                title=title,
                description=row['description'],
                img=img,
                stock=50,
                price=100.0,
            )

            # Add authors to the book
            book.authors.set(author_objects)

            # Add authors to the book
            for author in author_objects:
                book.authors.add(author)

            # Add categories to the book through the through model
            for category in category_objects:
                BooksCategories.objects.create(book=book, category=category)

            # Handle slug creation
            book.slug = slugify(book.title)
            book.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported books'))
