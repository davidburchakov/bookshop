from django.core.management.base import BaseCommand
import pandas as pd
import ast
from django.utils.text import slugify
from ...models.models import Books, Authors, Category, BooksCategories
import random
from datasets import load_dataset


class Command(BaseCommand):
    help = 'Import books from a CSV file into the database'
    def handle(self, *args, **options):

        dataset = load_dataset('spleentery/amazon_data_processed_4500.csv')
        data = dataset['train']
        df = data.to_pandas()
        # df = df.head(100)
        df.dropna(subset=['Title', 'description', 'authors', 'image', 'previewLink', 'categories', 'processed_title'],
                  inplace=True)
        print("number of entries: ", len(df))
        for index, row in df.iterrows():
            # Handle authors
            try:
                author_names = ast.literal_eval(row['authors'])
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
            random_stock = random.randint(0, 120)
            slug = slugify(title)
            previewLink = row['previewLink']
            publishedDate = row['publishedDate']
            publisher = row['publisher']


            # Check if the book with the same slug already exists
            if not Books.objects.filter(slug=slug).exists():
                # Only create a new book if a book with the same slug doesn't exist
                book = Books.objects.create(
                    title=title,
                    description=row['description'],
                    img=img,
                    stock=random_stock,
                    slug=slug,
                    previewLink=previewLink,
                    publishedDate=publishedDate,
                    publisher=publisher
                )

                # Add authors and categories to the book
                book.authors.set(author_objects)
                for category in category_objects:
                    BooksCategories.objects.create(book=book, category=category)
            else:
                self.stdout.write(f"Book '{title}' already exists in the database.")

        self.stdout.write(self.style.SUCCESS('Completed importing books'))