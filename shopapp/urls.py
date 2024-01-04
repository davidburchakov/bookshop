from django.urls import path
from shopapp.views.views import (index_view, about_view, faq_view, seneka_pg1)
from shopapp.views.book_view import books_view, single_book_view
from shopapp.views.cart_view import cart_view, add_to_cart, update_cart
from shopapp.views.user_view import (login_view, profile_view,
                                     register_view, logout_view,
                                     profile_update_view_page, profile_update_view,
                                     profile_delete)


urlpatterns = [
    path('', index_view, name='index'),
    path('index', index_view, name='index'),
    path('login', login_view, name='login'),
    path('register', register_view, name='register'),
    path('logout', logout_view, name='logout'),
    path("books", books_view, name='books'),
    path("book/<slug:slug>", single_book_view, name="book"),  # /posts/first-post
    path("profile", profile_view, name="profile"),
    path("profile-update-page", profile_update_view_page, name="profile-update-page"),
    path("profile-update", profile_update_view, name="profile-update"),
    path("profile-delete", profile_delete, name="profile-delete"),
    path("about", about_view, name="about"),
    path("faq", faq_view, name="faq"),
    path("cart", cart_view, name="cart"),
    path("add-to-cart", add_to_cart, name="add-to-cart"),
    path('update-cart/', update_cart, name='update-cart'),
    path('books/seneka/pg1', seneka_pg1, name="pg1")
]
