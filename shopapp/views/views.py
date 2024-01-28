from django.http import HttpRequest
from django.shortcuts import render
from .book_view import get_all_books
from django.db import connection
from .chatbot_view import get_recommended_books, get_most_popular_books

def get_all_faq():
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT EXISTS(
                SELECT FROM information_schema.tables
                WHERE table_schema='public'
                AND   table_name='shopapp_faq'
            );
        """)

        table_exists = cursor.fetchone()[0]
        faq_list = []
        if table_exists:
            cursor.execute("""
            SELECT question, answer FROM shopapp_faq; 
            """)
            rows = cursor.fetchall()
            faq_list = [{"question": row[0], "answer": row[1]} for row in rows]
        return faq_list


from ..models.models import Books
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
def get_all_books_paginator(page_num=1, books_per_page=30):
    books_qs = Books.objects.all().prefetch_related('authors').order_by('id')
    paginator = Paginator(books_qs, books_per_page)

    try:
        books_page = paginator.page(page_num)
    except PageNotAnInteger:
        books_page = paginator.page(1)
    except EmptyPage:
        books_page = paginator.page(paginator.num_pages)

    books = [
        {
            "slug": book.slug,
            "title": book.title,
            "img": book.img,
            "description": book.description,
            "stock": book.stock,
            "price": book.price,
            "id": book.id,
            "read": book.read,
            "authors": [author.fullname for author in book.authors.all()]
        } for book in books_page
    ]
    return books


faq = get_all_faq()
books = get_all_books()




def index_view(request: HttpRequest):
    page = request.GET.get('page', 1)  # Get the page number from query params
    most_popular_books = get_most_popular_books()
    recommended_books = get_recommended_books(request)
    books_page = get_all_books_paginator(page_num=page)  # Fetch the correct page
    context = {
        "books_page": books_page,  # This is already a paginated list of books
        "recommended_books": recommended_books,
        "most_popular_books": most_popular_books
    }
    # Check if the request is AJAX
    # Detect AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        books_page = get_all_books_paginator(page_num=page)  # Fetch the correct page
        print("AJAX DETECTED")
        return render(request, 'shopapp/books_list.html', {"books_page": books_page})

    return render(request, 'shopapp/shop-index.html', context=context)




def about_view(request: HttpRequest):
    return render(request, 'shopapp/about.html')


def faq_view(request: HttpRequest):
    context = {
        "faq": faq,
    }
    return render(request, "shopapp/faq.html", context=context)


def seneka_pg1(request: HttpRequest):
    return render(request, 'books/seneka/seneka-read.html')


