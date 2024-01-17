from ..models.models import Books, Rule
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from ..views.book_view import get_all_books
from django.shortcuts import get_object_or_404
import json
import nltk

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
books = get_all_books()


def preprocess_text(text):
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word.lower()) for word in tokens if word not in stop_words and word.isalpha()]
    return tokens


conversation_context = {}


def find_closest_match(user_input, user_id, request):
    if user_id in conversation_context and conversation_context[user_id]['action'] == 'confirm_add_to_cart':
        if 'yes' in user_input.lower():
            book_title = conversation_context[user_id]['book_title']
            book_id = conversation_context[user_id]['book_id']
            quantity = int(request.POST.get('quantity', 1))

            try:
                book = get_object_or_404(Books, pk=book_id)
                cart = request.session.get('cart', {})
                print("CART")
                print(cart)
                if book_id in cart:
                    cart[book_id]['quantity'] += quantity
                else:
                    cart[book_id] = {'quantity': quantity, 'price': str(book.price)}

                request.session['cart'] = cart
                total_quantity = sum(item['quantity'] for item in cart.values())
                del conversation_context[user_id]
                return f"'{book_title}' has been added to your cart."

            except Exception as e:
                del conversation_context[user_id]
                return "error occurred"

        else:
            # Clear the context if user responds with anything other than 'yes'
            del conversation_context[user_id]
            return "Okay, let me know if there is anything else I can help with."

    user_input_tokens = preprocess_text(user_input)
    highest_similarity = 0
    best_match = None

    for rule in Rule.objects.all():  # Query the database
        question_tokens = preprocess_text(rule.input)
        similarity = len(set(user_input_tokens) & set(question_tokens)) / len(
            set(user_input_tokens) | set(question_tokens))
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = rule.output
    if "add to cart" in user_input:
        for book in books:
            if book['title'].lower() in user_input.lower():
                conversation_context[user_id] = {'action': 'confirm_add_to_cart', 'book_title': book['title'],
                                                 'book_id': book['id']}
                return "Proceed with adding '" + book['title'] + "' to the cart?"

    return best_match or "I'm sorry, I don't understand your question."


def find_book_by_title(title):
    try:
        return Books.objects.get(title=title)
    except Books.DoesNotExist:
        return None


@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data['message']
        user_id = request.session.session_key
        bot_reply = find_closest_match(user_message, user_id, request)
        return JsonResponse({'reply': bot_reply})

    return JsonResponse({'reply': 'Invalid request'}, status=400)
