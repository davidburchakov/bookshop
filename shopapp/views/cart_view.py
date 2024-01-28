from django.shortcuts import render, redirect, get_object_or_404
from ..models.models import Books
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .chatbot_view import get_recommended_books, get_most_popular_books
from .book_view import get_all_books
import json


def add_to_cart(request):
    if request.method == 'POST' and request.user.is_authenticated:
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
                cart[book_id] = {'quantity': quantity, 'price': str(book.price), 'title': book.title}

            request.session['cart'] = cart
            total_quantity = sum(item['quantity'] for item in cart.values())
            return JsonResponse({'status': 'success', 'total_quantity': total_quantity})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'invalid request'}, status=400)


books = get_all_books()


def cart_view(request):

    if not books:
        context = {"error": "No books found"}
    else:
        most_popular_books = get_most_popular_books()
        recommended_books = get_recommended_books(request)
        context = {
            "books": books,
            "recommended_books": recommended_books,
            "most_popular_books": most_popular_books
        }

    return render(request, 'shopapp/cart.html', context)


def process_purchase(request):
    cart = request.session.get('cart', {})

    for book_id, data in cart.items():
        book = get_object_or_404(Books, id=book_id)
        new_stock = book.stock - data['quantity']
        print(data['quantity'])
        print(type(data['quantity'])) #int
        print("book id: ", book_id)
        print("book data\n", data)
        print("new stock: ", new_stock)
        book.stock = max(0, new_stock)  # Ensures stock doesn't go negative
        book.save()

    request.session['cart'] = {}
    return redirect('purchase_complete')  # Redirect to a confirmation page


def purchase_complete(request):
    # You can add any additional context or logic here if needed
    return render(request, 'shopapp/purchase_complete.html')

@require_POST
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
