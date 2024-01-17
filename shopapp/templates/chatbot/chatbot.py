import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from ...models.models import Rule

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


def preprocess_text(text):
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word.lower()) for word in tokens if word not in stop_words and word.isalpha()]
    return tokens


def find_closest_match(user_input):
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

    return best_match or "I'm sorry, I don't understand your question."
