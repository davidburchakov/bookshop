from timeit import default_timer
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.db import connection


def get_all_books():
    with connection.cursor() as cursor:
        # Updated query to join books with authors
        cursor.execute("""
            SELECT b.slug, a.fullname, b.title, b.img, b.description, b.stock
            FROM books b
            INNER JOIN authors a ON b.author_id = a.id
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


def index_view(request: HttpRequest):
    context = {
        "books": books
    }
    return render(request, 'shopapp/shop-index.html', context=context)


# Registration View
def register_view(request):
    print("register")
    if request.method == 'POST':
        print("POST")
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print("valid")
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')  # Redirect to a home page
    else:
        form = UserCreationForm()
    # return render(request, 'authapp/register.html', {'form': form})
    return render(request, 'shopapp/register.html', context={"form": form})


# Login View
def login_view(request: HttpRequest):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to a home page
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'shopapp/login.html')


def profile_view(request: HttpRequest):
    context = {
        'request': request,
        'user': request.user
    }
    return render(request, 'user/profile.html', context=context)

def logout_view(request):
    logout(request)
    return redirect('index')  # Redirects to the home page after logout


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
