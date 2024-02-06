import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import datetime
import random
from ...models.models import UserProfile, Books, Review
from datasets import load_dataset

class Command(BaseCommand):
    help = 'Import users, books, and reviews from a CSV file'

    def handle(self, *args, **options):
        dataset = load_dataset('spleentery/books_ratings')
        data = dataset['train']
        df = data.to_pandas()
        df = df.head(100)

        for _, row in df.iterrows():
            # Create or get user
            profile_name = row['profileName'].strip()
            email = f"{profile_name.replace(' ', '_')}@gmail.com"
            phone = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            user, user_created = User.objects.get_or_create(username=profile_name, email=email)
            if user_created:
                user.set_password('rhengh79!A')
                user.save()
                UserProfile.objects.create(user=user, phone=phone)
                self.stdout.write(self.style.SUCCESS(f'User {profile_name} CREATED'))
            else:
                self.stdout.write(self.style.ERROR(f'User {profile_name} already exists'))

            # Create or get book
            book_title = row['Title'].strip()[:255]
            book_slug = slugify(book_title)
            book_price = float(row['Price'])
            book, book_created = Books.objects.get_or_create(
                slug=book_slug,
                defaults={'title': book_title, 'price': book_price}
            )

            if not book_created:
                book.price = book_price
                book.save()
                self.stdout.write(self.style.SUCCESS(f'Book {book_title} already exists. Updating price...'))

            # Create or update review
            review_time = datetime.fromtimestamp(int(row['review/time']))
            print("REVIEW TIME:", review_time)
            review_text = row['review/text'].strip()
            review_summary = row['review/summary'].strip()
            review_score = float(row['review/score'])
            review, review_created = Review.objects.update_or_create(
                book=book,
                user=user,
                defaults={
                    'text': review_text,
                    'summary': review_summary,
                    'score': review_score,
                    'created_at': review_time
                }
            )

            if review_created:
                self.stdout.write(self.style.SUCCESS(f"{profile_name}'s review created"))

            if user_created or book_created or review_created:
                self.stdout.write(self.style.SUCCESS(f'Entry created/updated for user: {profile_name}, book: {book_title}'))

        self.stdout.write(self.style.SUCCESS('Successfully imported users, books, and reviews'))
