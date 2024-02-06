from ..models.models import Books
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..views.book_view import get_all_books
from django.db.models import Count, Avg
import json
import numpy as np
import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from django.conf import settings
from datasets import load_dataset


# load book df
dataset = load_dataset('spleentery/amazon_data_processed_4500.csv')
data = dataset['train']
book_df = data.to_pandas()
book_df.dropna(subset=['Title', 'description', 'authors', 'image', 'previewLink', 'categories', 'processed_title'],
          inplace=True)


book_title = (
    "Python Programming with the Java Class Libraries: A Tutorial for Building Web and Enterprise Applications "
    "with Jython")

doc_sim_path = os.path.join(settings.BASE_DIR, 'shopapp', 'static', 'nlp', 'doc_sim_df.csv.gz')
doc_sim_df = pd.read_csv(doc_sim_path, compression='gzip')

books_list = book_df['Title'].values


def get_recommended_books_titles(b_title=book_title, list_books=books_list, doc_sims=doc_sim_df):
    if b_title in list_books:
        book_idx = np.where(list_books == b_title)[0][0]
        book_similarities = doc_sims.iloc[book_idx].values
        similar_book_idxs = np.argsort(-book_similarities)[1:6]  # get top 5 similar book IDs
        similar_books = list_books[similar_book_idxs]
        return list(similar_books)
    else:
        print(f"Book title '{b_title}' not found in the books list.")
        # Handle the case where book title is not found
        # Maybe return a default list or an empty list
        return []



def get_recommended_books(request):
    books = get_all_books()
    recommended_books = []
    try:
        cart = request.session.get('cart', {})
        if cart:
            for key, value in cart.items():
                recommended_book_title = value.get('title')
                if recommended_book_title:
                    recommended_books_titles = get_recommended_books_titles(recommended_book_title)
                    for book in books:
                        if book['title'] in recommended_books_titles:
                            recommended_books.append(book)
        else:
            recommended_books_titles = get_recommended_books_titles()
            for book in books:
                if book['title'] in recommended_books_titles:
                    recommended_books.append(book)
    except:
        recommended_books_titles = get_recommended_books_titles()
        for book in books:
            if book['title'] in recommended_books_titles:
                recommended_books.append(book)
    return recommended_books


def get_most_popular_books():
    # Annotate books with their review count and average score
    books_with_stats = Books.objects.annotate(
        review_count=Count('review'),
        average_score=Avg('review__score')
    )

    # First, get the books with the most reviews
    most_reviewed_books = books_with_stats.order_by('-review_count')

    # From these, take the top 15
    top_15_most_reviewed = most_reviewed_books[:15]

    # Then, sort these top 15 books by their average score in descending order
    # Treat None as the lowest possible value
    top_books_sorted_by_score = sorted(
        top_15_most_reviewed,
        key=lambda x: x.average_score if x.average_score is not None else float('-inf'),
        reverse=True
    )

    return top_books_sorted_by_score



# ---------------------------- Openai and tf-idf ----------------------------


@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data['message']
        user_id = request.session.session_key
        title, description, authors = find_most_similar_book(user_message)

        response_message = get_chatgpt_response(user_id, title, description, authors)
        return JsonResponse({'reply': response_message})

    return JsonResponse({'reply': 'Invalid request'}, status=400)


# pip install openai
from openai import OpenAI
from decouple import config

def get_chatgpt_response(chat_prompt, title, description, authors):
    temperature = .9
    number_of_examples = 5

    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key=config('API_KEY'),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""you are an online chatbot assistant of a book store. Try to help the customer 
                by providing book recommendations. 
                Generate no more than 30 words. Consider you know the following information about the book:
                Title: {title}
                description: {description}
                authors: {authors}
                original message: {chat_prompt}"""
            }
        ],
        model="gpt-3.5-turbo",
    )

    return chat_completion.choices[0].message.content



# Preprocessing
from nltk.corpus import stopwords

# nltk.download('stopwords')
stop_words = set(stopwords.words('english'))


def preprocess(text):
    text = text.lower()  # Lowercasing
    tokens = nltk.word_tokenize(text)  # Tokenization
    tokens = [word for word in tokens if word.isalpha()]  # Remove non-alphabetic tokens
    tokens = [word for word in tokens if not word in stop_words]  # Remove stopwords
    return " ".join(tokens)


# Vectorization
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(book_df['processed_title'])


# Function to find most similar book
def find_most_similar_book(query, vectorizer_fun=vectorizer, tfidf_matrix_fun=tfidf_matrix):
    pass
    query = preprocess(query)
    query_vec = vectorizer_fun.transform([query])
    cosine_similarities = cosine_similarity(query_vec, tfidf_matrix_fun).flatten()
    most_similar_book_index = np.argmax(cosine_similarities)
    return (book_df.iloc[most_similar_book_index]['Title'],
            book_df.iloc[most_similar_book_index]['description'],
            book_df.iloc[most_similar_book_index]['authors'])
