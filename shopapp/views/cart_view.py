from django.shortcuts import render, redirect, get_object_or_404
from ..models.models import Books
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json


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
