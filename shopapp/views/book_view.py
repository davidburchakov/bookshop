# books_view.py
from collections import defaultdict
from django.http import HttpRequest
from django.shortcuts import render
from django.http import JsonResponse
from ..models.models import Review, Books, Category
from django.db.models import Avg
from django.core.exceptions import ValidationError


def get_all_books():
    books = Books.objects.all().prefetch_related('authors')
    return [
        {
            "slug": book.slug,
            "title": book.title,
            "img": book.img,
            "description": book.description,
            "stock": book.stock,
            "price": book.price,
            "id": book.id,
            "read": book.read,
            "authors": [author.fullname for author in book.authors.all()],
            "previewLink": book.previewLink,
            "publishedDate": book.publishedDate,
            "publisher": book.publisher,
        } for book in books
    ]


def get_all_categories():
    return {category.id: category.name for category in Category.objects.all()}


def get_categories_by_id(book_id):
    book = Books.objects.filter(id=book_id).prefetch_related('categories').first()
    if book:
        return {"categories": [category.name for category in book.categories.all()]}
    return {"categories": []}


def get_all_book_categories():
    book_categories = defaultdict(list)
    books = Books.objects.prefetch_related('categories')

    for book in books:
        for category in book.categories.all():
            book_categories[book.id].append(category.name)

    return dict(book_categories)


from django.db.models import Q


def search_books_by_query(all_books, query):
    return [
        book for book in all_books if
        query in book['title'].lower() or query in book['description'].lower()
    ]


def single_book_view(request: HttpRequest, slug):
    books = get_all_books()
    book = [i for i in books if i["slug"] == slug][0]
    categories = get_categories_by_id(book['id'])
    categories['categories'] = categories['categories']
    reviews = Review.objects.filter(book_id=book['id']).order_by('-created_at')
    average_score = Review.objects.filter(book=book['id']).aggregate(Avg('score'))['score__avg']
    if average_score is not None:
        average_score = round(average_score, 2)
    else:
        average_score = "Not yet rated"

    context = {
        "book": book,
        "categories": categories['categories'],
        "reviews": reviews,
        "review_length": len(reviews),
        "average_score": average_score,
        "range_5": reversed(range(1, 6)),
        "list_5": list(reversed(range(1, 6))),
    }
    return render(request, "shopapp/book.html", context=context)


def submit_score(request):
    if request.method == 'POST':
        try:
            book_id = request.POST.get('book_id')
            score_value = request.POST.get('score')

            # Convert book_id and score to integers and validate
            book_id = int(book_id)
            score_value = int(score_value)
            if score_value < 1 or score_value > 5:
                raise ValidationError("Score must be between 1 and 5")

            book = Books.objects.get(id=book_id)

            if request.user.is_authenticated:
                # For authenticated users, update or create a review with the score
                review, created = Review.objects.update_or_create(
                    book=book, user=request.user,
                    defaults={'score': score_value, 'text': ''})  # You can keep text empty or handle it differently
            else:
                # For anonymous users, handle session-based scoring
                session_id = request.session.session_key or request.session.create()
                review, created = Review.objects.update_or_create(
                    book=book, session_id=session_id,
                    defaults={'score': score_value, 'text': ''})

            average_score = Review.objects.filter(book=book).aggregate(Avg('score'))['score__avg']
            if average_score is not None:
                average_score = round(average_score, 2)

            return JsonResponse({'status': 'success', 'average_score': average_score})

        except Books.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Book not found'})
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid data'})
        except ValidationError as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def browse_view(request: HttpRequest):
    books = get_all_books()
    filtered_books = books
    free_read_filter = request.GET.get('free', 'off') == 'on'
    available_stock_filter = request.GET.get('available_stock', 'off') == 'on'
    category_filter = request.GET.get('category', 'none')
    book_category = get_all_book_categories()

    query = request.GET.get('search_query', '')
    if query:
        filtered_books = search_books_by_query(books, query)

    if free_read_filter:
        filtered_books = [book for book in filtered_books if book['read']]

    if available_stock_filter:
        filtered_books = [book for book in filtered_books if int(book['stock']) > 0]

    if category_filter != 'none':
        filtered_books = [book for book in filtered_books if
                          book_category.get(book['id']) and
                          category_filter.lower() == book_category.get(book['id'], [''])[0].lower()]

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
    categories = get_all_categories()
    books_count = len(filtered_books)
    context = {
        "books": filtered_books,
        "categories": categories,
        "books_count": books_count
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
        score = request.POST.get('score', None)  # Score is optional

        try:
            book = Books.objects.get(id=book_id)
            # Create a new review instance every time
            review = Review.objects.create(
                book=book,
                user=request.user,
                text=text,
                score=int(score) if score else None
            )

            return JsonResponse({
                'status': 'success',
                'review': review.text,
                'username': request.user.username,  # Add username to the response
                'createdAt': review.created_at.strftime("%Y-%m-%d %H:%M")  # Format the datetime
            })

        except Books.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Book not found'})
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid data'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
