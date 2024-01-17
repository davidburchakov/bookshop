from django.urls import path
from shopapp.views.cookies_view import set_cookie_consent
from shopapp.views.views import (index_view, about_view, faq_view)
from shopapp.views.book_view import books_view, single_book_view, browse_view, post_review, submit_score
from shopapp.views.cart_view import cart_view, add_to_cart, update_cart
from shopapp.views.seneka_view import pdf_view, letter_view
from shopapp.views.user_view import (login_view, profile_view,
                                     register_view, logout_view,
                                     profile_update_view_page, profile_update_view,
                                     profile_delete, password_change_view_page, password_change_view)


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
    path('books/seneka/seneka-read', pdf_view, name="seneka-read"),
    path('books/seneka/letter/<str:letter_id>/', letter_view, name='letter'),
    path("browse", browse_view, name="browse"),
    path('set-cookie-consent/', set_cookie_consent, name='set_cookie_consent'),
    path('password-change-page', password_change_view_page, name='password-change-page'),
    path("password-change", password_change_view, name='password-change'),
    path('post-review/<int:book_id>/', post_review, name='post_review'),
    path("submit-score", submit_score, name='submit-score')

]
