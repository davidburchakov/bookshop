from django.http import HttpRequest
from django.shortcuts import render
from django.db import connection
from django.db.models import Q
from ..models.models import Books


def get_all_books():
    books = []
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

        if table_exists:
            cursor.execute("""
                SELECT b.slug, a.fullname, b.title, b.img, b.description, b.stock, b.price, b.id, b.read, b.language, b.original_language, a.country_id, c.name
                FROM shopapp_books b
                INNER JOIN shopapp_authors a ON b.author_id = a.id
                INNER JOIN shopapp_country c ON a.country_id = c.id
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
                    "stock": row[5],
                    "price": row[6],
                    "id": row[7],
                    "read": row[8],
                    "language": row[9],
                    "original_language": row[10],
                    "country_id": row[11],
                    "country_name": row[12]
                } for row in rows
            ]
    return books


books = get_all_books()


def get_all_categories(book_id):
    categories = {"categories": []}
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = 'shopapp_category'
                );
        """)

        table_exists = cursor.fetchone()[0]

        if table_exists:
            cursor.execute("""
                SELECT c.name
                FROM shopapp_bookscategories b
                INNER JOIN shopapp_books a on a.id = b.book_id
                INNER JOIN shopapp_category c ON b.category_id = c.id
                WHERE a.id = %s
            """, [book_id])

            rows = cursor.fetchall()
            for row in rows:
                categories['categories'].append(row[0])
    return categories


def books_view(request: HttpRequest):
    context = {
        # "products": products
    }
    return render(request, 'shopapp/books.html', context=context)


def single_book_view(request: HttpRequest, slug):
    book = [i for i in books if i["slug"] == slug][0]
    categories = get_all_categories(book['id'])
    context = {
        "book": book,
        "categories": categories['categories']
    }
    return render(request, "shopapp/book.html", context=context)


def browse_view(request: HttpRequest):
    country_filter = request.GET.get('country', 'none')
    free_read_filter = request.GET.get('free', 'off') == 'on'
    available_stock_filter = request.GET.get('available_stock', 'off') == 'on'
    available_language_filter = request.GET.get('available_language', 'none')
    category_filter = request.GET.get('category', 'none')

    if free_read_filter:
        filtered_books = [book for book in books if book['read']]
    else:
        filtered_books = books

    if available_stock_filter:
        filtered_books = [book for book in books if int(book['stock']) > 0]

    if country_filter != 'none':
        filtered_books = [book for book in filtered_books if book['country_name'].lower() == country_filter]

    if available_language_filter != 'none':
        filtered_books = [book for book in filtered_books if book['language'].lower() == available_language_filter]

    if category_filter != 'none':
        filtered_books = [book for book in filtered_books if
                          category_filter.lower() in [b.lower() for b in get_all_categories(book['id'])['categories']]]

    try:
        min_price = int(request.GET.get('min_price', '10'))
        if min_price < 0:
            min_price = 10
    except ValueError:
        min_price = 10

    try:
        max_price = int(request.GET.get('max_price', '200'))
        if max_price < 0:
            max_price = 200
    except ValueError:
        max_price = 200

    # Ensure min_price is not greater than max_price
    if min_price > max_price:
        min_price, max_price = 10, 200
    print("min price:", min_price)
    print("max price:", max_price)
    filtered_books = [book for book in filtered_books if min_price <= book['price'] <= max_price]

    context = {
        "books": filtered_books
    }
    return render(request, 'shopapp/browse.html', context=context)


def search_books(request):
    query = request.GET.get('search-query', '')

    # Perform full-text search in title and description fields
    books = Books.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )

    context = {'books': books}
    return render(request, 'shopapp/browse.html', context)
