from django.http import HttpRequest
from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
from ..models.models import Review, Books, Score
from django.db.models import Avg
from django.core.exceptions import ValidationError


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
                SELECT b.slug, b.title, b.img, b.description, b.stock, b.price, b.id, b.read, 
                       ARRAY_AGG(a.fullname) as authors
                FROM shopapp_books b
                INNER JOIN shopapp_books_authors ba ON b.id = ba.books_id
                INNER JOIN shopapp_authors a ON ba.authors_id = a.id
                GROUP BY b.slug, b.title, b.img, b.description, b.stock, b.price, b.id, b.read
            """)
            rows = cursor.fetchall()

            # Mapping rows to a list of dictionaries
            books = [
                {
                    "slug": row[0],
                    "title": row[1],
                    "img": row[2],
                    "description": row[3],
                    "stock": row[4],
                    "price": row[5],
                    "id": row[6],
                    "read": row[7],
                    "authors": row[8]  # This will be a list of author names
                } for row in rows
            ]
    return books


books = get_all_books()


def get_all_categories():
    categories = {}
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
                    SELECT id, name
                    FROM shopapp_category
                """)

            rows = cursor.fetchall()
            for row in rows:
                categories[row[0]] = row[1]
    return categories


categories = get_all_categories()


def get_categories_by_id(book_id):
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


def get_all_book_categories():
    book_categories = {}
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = 'shopapp_bookscategories'
            );
        """)

        table_exists = cursor.fetchone()[0]

        if table_exists:
            cursor.execute("""
                SELECT a.id, c.name
                FROM shopapp_books a
                LEFT JOIN shopapp_bookscategories b ON a.id = b.book_id
                LEFT JOIN shopapp_category c ON b.category_id = c.id
            """)

            rows = cursor.fetchall()
            for book_id, category_name in rows:
                if book_id not in book_categories:
                    book_categories[book_id] = []
                if category_name:  # Check if category_name is not None
                    book_categories[book_id].append(category_name)

    return book_categories

book_category = get_all_book_categories()


def books_view(request: HttpRequest):
    context = {
        # "products": products
    }
    return render(request, 'shopapp/books.html', context=context)


def single_book_view(request: HttpRequest, slug):
    book = [i for i in books if i["slug"] == slug][0]
    categories = get_categories_by_id(book['id'])
    categories['categories'] = categories['categories']
    reviews = Review.objects.filter(book_id=book['id'])
    # To store scores for each review
    review_scores = {review.id: review.scores.first().score for review in reviews if review.scores.exists()}
    # Calculate the average score for the book
    average_score = Score.objects.filter(review__book=book['id']).aggregate(Avg('score'))['score__avg'] or "Not yet rated"
    context = {
        "book": book,
        "categories": categories['categories'],
        "reviews": reviews,
        "average_score": average_score,
        "review_scores": review_scores,
        "range_5": reversed(range(1, 6))
    }
    return render(request, "shopapp/book.html", context=context)


def browse_view(request: HttpRequest):
    filtered_books = books
    free_read_filter = request.GET.get('free', 'off') == 'on'
    available_stock_filter = request.GET.get('available_stock', 'off') == 'on'
    category_filter = request.GET.get('category', 'none')
    print("books length")
    print(len(books))
    query = request.GET.get('search_query', '')
    if query:
        filtered_books = search_books_by_query(books, query)

    if free_read_filter:
        filtered_books = [book for book in filtered_books if book['read']]

    if available_stock_filter:
        filtered_books = [book for book in filtered_books if int(book['stock']) > 0]

    if category_filter != 'none':
        filtered_books = [book for book in filtered_books if
                          book_category[book['id']] and
                          category_filter.lower() == book_category[book['id']][0].lower()]

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

    filtered_books = [book for book in filtered_books if min_price <= book['price'] <= max_price]

    context = {
        "books": filtered_books,
        "categories": categories
    }
    return render(request, 'shopapp/browse.html', context=context)


def search_books_by_query(all_books, query):
    query = query.lower()
    filtered_books = []

    for book in all_books:
        if query in book['title'].lower() or query in book['description'].lower():
            filtered_books.append(book)

    return filtered_books


def post_review(request, book_id):
    if request.method == 'POST' and request.user.is_authenticated:
        text = request.POST.get('text')
        try:
            book = Books.objects.get(id=book_id)
            review = Review.objects.create(book=book, user=request.user, text=text)
            print("REVIEW CREATED")
            return JsonResponse({'status': 'success', 'review': review.text})
        except Books.DoesNotExist:
            print("BOOK NOT FOUND. REVIEW")
            return JsonResponse({'status': 'error', 'message': 'Book not found'})
    print("REVIEW INVALID REQUEST")
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def submit_score(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            book_id = request.POST.get('book_id')
            score = request.POST.get('score')

            # Validate that book_id is an integer
            book_id = int(book_id)

            # Validate that score is an integer and within the expected range
            score = int(score)
            if score < 1 or score > 5:
                raise ValidationError("Score must be between 1 and 5")

            # Check if the book exists
            book = Books.objects.get(id=book_id)

            # Check if the user has already submitted a score for this book
            existing_score = Score.objects.filter(book=book, user=request.user).first()

            if existing_score:
                existing_score.score = score
                existing_score.save()
            else:
                Score.objects.create(book=book, user=request.user, score=score)

            # Calculate and return the average score
            average_score = Score.objects.filter(book=book).aggregate(Avg('score'))['score__avg']
            return JsonResponse({'status': 'success', 'average_score': average_score})

        except Books.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Book not found'})
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid data'})
        except ValidationError as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request or not authenticated'})
