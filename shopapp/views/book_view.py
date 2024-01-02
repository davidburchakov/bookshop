from django.http import HttpRequest
from django.shortcuts import render
from django.db import connection

def get_all_books():
    with connection.cursor() as cursor:
        # Check if the 'books' table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE  table_schema = 'public'
                AND    table_name   = 'shopapp_books'
            );
        """)
        table_exists = cursor.fetchone()[0]

        books = []
        if table_exists:
            # Query to join books with authors
            cursor.execute("""
                SELECT b.slug, a.fullname, b.title, b.img, b.description, b.stock
                FROM shopapp_books b
                INNER JOIN shopapp_authors a ON b.author_id = a.id
            """)
            rows = cursor.fetchall()

            # Mapping rows to a list of dictionaries
            books = [
                {
                    "slug": row[0],
                    "author": row[1],
                    "title": row[2],
                    "img": row[3],
                    "description": row[4],
                    "stock": row[5]
                } for row in rows
            ]
        return books

books = get_all_books()



def books_view(request: HttpRequest):
    products = {'Dostoyevsky': 1999, 'Tolstoy': 2000, 'Kamus': 30000, 'Kafka': 1}
    context = {
        "products": products
    }
    return render(request, 'shopapp/books.html', context=context)


def single_book_view(request: HttpRequest, slug):
    book = [i for i in books if i["slug"] == slug][0]
    context = {
        "book": book
    }
    return render(request, "shopapp/book.html", context=context)

