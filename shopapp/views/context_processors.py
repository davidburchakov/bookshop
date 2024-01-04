from django.shortcuts import get_object_or_404
from ..models.models import Books

def cart_context_processor(request):
    cart = request.session.get('cart', {})
    books_in_cart = []
    final_price = 0.0
    total_quantity = 0
    for book_id, data in cart.items():
        book = get_object_or_404(Books, pk=book_id)
        total_price = float(data['price']) * data['quantity']
        final_price += total_price
        quantity = data['quantity']
        total_quantity += quantity
        books_in_cart.append({
            'book': book,
            'quantity': quantity,
            'total_price': total_price
        })

    return {
        'cart_books_in_cart': books_in_cart,
        'cart_final_price': final_price,
        'total_quantity': total_quantity
    }
