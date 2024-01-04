import PyPDF2
from django.shortcuts import render


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text


def split_text_into_chunks(text, max_words=1000):
    words = text.split()
    for i in range(0, len(words), max_words):
        yield ' '.join(words[i:i + max_words])


import os
from django.conf import settings

pdf_path = os.path.join(settings.BASE_DIR, 'shopapp/views/letters-from-a-stoic_lucius-annaeus-seneca.pdf')
text = extract_text_from_pdf(pdf_path)
pages = list(split_text_into_chunks(text, 5000))


def pdf_view(request):
    return render(request, 'books/seneka/pg1.html', {'pages': pages})
