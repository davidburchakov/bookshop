from ..models.models import Books, Rule
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from ..views.book_view import get_all_books
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count
import json
import numpy as np
import pandas as pd
import nltk

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
books = get_all_books()


def preprocess_text(text):
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word.lower()) for word in tokens if word not in stop_words and word.isalpha()]
    return tokens


conversation_context = {}


def update_quantity(total_quantity):
    return JsonResponse({'status': 'success', 'total_quantity': total_quantity})


def find_closest_match(user_input, user_id, request):
    if user_id in conversation_context and conversation_context[user_id]['action'] == 'confirm_add_to_cart':
        if 'yes' in user_input.lower():
            book_title = conversation_context[user_id]['book_title']
            book_id = str(conversation_context[user_id]['book_id'])
            quantity = int(request.POST.get('quantity', 1))

            try:
                book = get_object_or_404(Books, pk=book_id)
                cart = request.session.get('cart', {})
                if book_id in cart:
                    current_quantity = int(cart[book_id]['quantity'])
                    updated_quantity = current_quantity + 1
                    cart[book_id] = {'quantity': updated_quantity, 'price': str(book.price)}
                else:
                    cart[book_id] = {'quantity': quantity, 'price': str(book.price)}
                request.session['cart'] = cart
                del conversation_context[user_id]
                return f"'{book_title}' has been added to your cart."

            except Exception as e:
                del conversation_context[user_id]
                return f"error occurred {e}"

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
                return "Proceed with adding '" + book['title'] + "' to the cart? (yes/no)"

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
        response_message = find_closest_match(user_message, user_id, request)

        return JsonResponse({'reply': response_message})

    return JsonResponse({'reply': 'Invalid request'}, status=400)


import os
from django.conf import settings

book_title = ("Python Programming with the Java Class Libraries: A Tutorial for Building Web and Enterprise Applications "
           "with Jython")

doc_sim_path = os.path.join(settings.BASE_DIR, 'shopapp', 'static', 'nlp', 'doc_sim_df_NOT_compressed.csv.gz')
doc_sim_df = pd.read_csv(doc_sim_path, compression='gzip')

amazon_books_path = os.path.join(settings.BASE_DIR, 'amazon_books_data_4500.csv')
amazon_book_df = pd.read_csv(amazon_books_path)

books_list = amazon_book_df['Title'].values


def get_recommended_books_titles(b_title=book_title, list_books=books_list, doc_sims=doc_sim_df):

    book_idx = np.where(list_books == b_title)[0][0]
    book_similarities = doc_sims.iloc[book_idx].values
    similar_book_idxs = np.argsort(-book_similarities)[1:6] # get top 5 similar book IDs
    similar_books = list_books[similar_book_idxs]

    return list(similar_books)


def get_recommended_books(request):
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


from django.db.models import Count, Avg


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
    top_books_sorted_by_score = sorted(top_15_most_reviewed, key=lambda x: x.average_score, reverse=True)

    return top_books_sorted_by_score


# ---------------------------- Word2Vec/Gensim ----------------------------

# descriptions = [book['description'] for book in books]
# descriptions_df = pd.DataFrame(descriptions, columns=['Description'])
#
# descriptions_df.to_csv('bookshop_descriptions.csv', index=False)
#
#
#
#
# from gensim.models import Word2Vec
# import nltk
# from nltk.tokenize import WordPunctTokenizer
# # import time
# # start_time = time.time()
# # Tokenize sentences in the 'Review' column of the corpus
# wpt = WordPunctTokenizer()
# tokenized_corpus = [wpt.tokenize(document) for document in descriptions_df['Description']]
#
# # Set values for various parameters
# feature_size = 100  # Word vector dimensionality
# window_context = 30  # Context window size
# min_word_count = 5  # Minimum word count
# sample = 1e-3  # Downsample setting for frequent words
#
# # Initialize and train the model (this may take some time)
# w2v_model = Word2Vec(vector_size=feature_size,
#                      window=window_context,
#                      min_count=min_word_count,
#                      sample=sample,
#                      epochs=50)
#
# # Build the vocabulary and train the Word2Vec model
# w2v_model.build_vocab(tokenized_corpus)
# w2v_model.train(tokenized_corpus, total_examples=w2v_model.corpus_count, epochs=w2v_model.epochs)
#
#
#
# from sklearn.metrics.pairwise import cosine_similarity
# from nltk.tokenize import WordPunctTokenizer
#
# def sentence_similarity(sentence1, sentence2, w2v_model):
#
#     # processed_sentence1 = process_sentence(sentence1)
#     # processed_sentence2 = process_sentence(sentence2)
#     processed_sentence1 = sentence1
#     processed_sentence2 = sentence2
#
#     tokenizer = WordPunctTokenizer()
#
#     # Tokenize sentences
#     words1 = tokenizer.tokenize(processed_sentence1)
#     words2 = tokenizer.tokenize(processed_sentence2)
#
#     # Compute average vector for each sentence
#     vector1 = np.mean([w2v_model.wv[word] for word in words1 if word in w2v_model.wv] or [np.zeros(w2v_model.vector_size)], axis=0)
#     vector2 = np.mean([w2v_model.wv[word] for word in words2 if word in w2v_model.wv] or [np.zeros(w2v_model.vector_size)], axis=0)
#
#     # Compute cosine similarity and convert it to percentage
#     similarity = cosine_similarity([vector1], [vector2])[0][0]
#     return (similarity + 1) / 2 * 100
#
# # Example usage
# sentence1 = "The story follows Harry Potter, a young wizard who discovers his magical heritage as he makes close friends and a few enemies in his first year at the Hogwarts School of Witchcraft and Wizardry."
# sentence2 = "Harry Potter and the Half-Blood Prince, the sixth book in the Harry Potter series by J.K. Rowling, delves into the history of Lord Voldemort's dark past and Harry's preparations for the final battle against him."
#
# # Assuming w2v_model is your Word2Vec model
# similarity_percentage = sentence_similarity(sentence1, sentence2, w2v_model)
# print(f"The similarity between the sentences is: {similarity_percentage:.2f}%")
#
#
#
# def recommend_book_by_description(user_input):
#     highest_similarity = 0
#     best_match = None
#
#     for book in books:  # Assuming books is a list of books with descriptions
#         book_description = book['description']
#         similarity = sentence_similarity(user_input, book_description, w2v_model)
#
#         if similarity > highest_similarity:
#             highest_similarity = similarity
#             best_match = book
#
#     return best_match
