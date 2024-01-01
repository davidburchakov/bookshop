from django.http import HttpRequest
from django.shortcuts import render
from .book_view import get_all_books

books = get_all_books()

def index_view(request: HttpRequest):
    context = {
        "books": books
    }
    return render(request, 'shopapp/shop-index.html', context=context)



def about_view(request: HttpRequest):
    return render(request, 'shopapp/about.html')

def faq_view(request: HttpRequest):
    return render(request, "shopapp/faq.html")