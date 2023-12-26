from django.urls import path
from .views import (index_view, login_view,
                    register_view, logout_view,
                    books_view, single_book_view,
                    profile_view, )

urlpatterns = [
    path('', index_view, name='index'),
    path('index', index_view, name='index'),
    path('login', login_view, name='login'),
    path('register', register_view, name='register'),
    path('logout', logout_view, name='logout'),
    path("books", books_view, name='books'),
    path("book/<slug:slug>", single_book_view, name="book"),  # /posts/first-post
    path("profile", profile_view, name="profile"),
]
