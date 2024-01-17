from django.http import HttpRequest
from django.shortcuts import render
from .book_view import get_all_books
from django.db import connection
from django.http import JsonResponse
from ..templates.chatbot.chatbot import find_closest_match
from django.views.decorators.csrf import csrf_exempt
import json

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
    if not books:
        context = {"error": "No books found"}
    else:
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


def seneka_pg1(request: HttpRequest):
    return render(request, 'books/seneka/seneka-read.html')


@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data['message']
        bot_reply = find_closest_match(user_message)
        return JsonResponse({'reply': bot_reply})

    return JsonResponse({'reply': 'Invalid request'}, status=400)
