from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .book_view import get_all_books
from django.db import connection
from ..models.models import Books


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


faq = get_all_faq()
books = get_all_books()


def index_view(request: HttpRequest):
    context = {
        "books": books
    }
    return render(request, 'shopapp/shop-index.html', context=context)


def about_view(request: HttpRequest):
    return render(request, 'shopapp/about.html')


def faq_view(request: HttpRequest):
    context = {
        "faq": faq,
    }
    return render(request, "shopapp/faq.html", context=context)


def add_to_cart(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        if not book_id.isdigit():
            return JsonResponse({'status': 'error', 'message': 'Invalid book ID'})

        quantity = int(request.POST.get('quantity', 1))

        try:
            book = get_object_or_404(Books, pk=book_id)
            cart = request.session.get('cart', {})

            if book_id in cart:
                cart[book_id]['quantity'] += quantity
            else:
                cart[book_id] = {'quantity': quantity, 'price': str(book.price)}

            request.session['cart'] = cart

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'invalid request'}, status=400)


def cart_view(request):
    return render(request, 'shopapp/cart.html')


def process_purchase(request):
    cart = request.session.get('cart', {})

    for book_id, data in cart.items():
        book = get_object_or_404(Books, id=book_id)
        book.stock -= data['quantity']
        book.save()

    request.session['cart'] = {}
    return redirect('purchase_complete')  # Redirect to a confirmation page



from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

@require_POST
@csrf_exempt
def update_cart(request):
    try:
        data = json.loads(request.body)
        book_id = str(data.get('book_id'))
        change = data.get('change', 0)

        cart = request.session.get('cart', {})
        if book_id in cart:
            new_quantity = cart[book_id]['quantity'] + change
            if new_quantity < 1:
                del cart[book_id]  # Remove the item from the cart
            else:
                cart[book_id]['quantity'] = new_quantity  # Update the quantity
            request.session['cart'] = cart
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Book not in cart'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
