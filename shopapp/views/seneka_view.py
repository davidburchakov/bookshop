import re
import PyPDF2
from django.shortcuts import render

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

def split_text_by_letter(text):
    # This pattern matches the word "LETTER" followed by a space and a Roman numeral
    pattern = r'(?i)(LETTER\s+[IVXLCDM]+)'
    # Split the text by the pattern, capturing the delimiters in the result
    parts = re.split(pattern, text)
    # The first item in the list will be an empty string if the text starts with a heading
    if parts[0] == '':
        parts = parts[1:]
    # Combine each delimiter with the text that follows it
    for i in range(0, len(parts), 2):
        yield (parts[i], parts[i+1])  # Returns a tuple of (LETTER XX, text)



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
    pdf_path = os.path.join(settings.BASE_DIR, 'shopapp/views/letters-from-a-stoic_lucius-annaeus-seneca.pdf')
    text = extract_text_from_pdf(pdf_path)
    letters = list(split_text_by_letter(text))
    return render(request, 'books/seneka/pg1.html', {'letters': letters})
