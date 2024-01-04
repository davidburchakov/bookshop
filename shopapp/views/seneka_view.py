import re
import PyPDF2
from django.shortcuts import render

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages[13:]:
            text += page.extract_text() + "\n"
        return text

import re

def split_text_by_letter(text):
    pattern = r'(LETTER [IVXLCDM]+)'
    parts = re.split(pattern, text)
    letters_dict = {}
    if parts:
        if parts[0].strip() == '':
            parts.pop(0)
        if parts[0].strip() == 'LETTERS':
            parts.pop(0)
        # Ensure that we only iterate up to the second-to-last element to avoid IndexError
        for i in range(0, len(parts) - 1, 2):
            heading = parts[i].strip()
            content = parts[i+1].strip() if i + 1 < len(parts) else ""
            letters_dict[heading] = content
    print(letters_dict.values())
    return letters_dict

# Test the function with some text
test_text = """
    LETTER XXX
    Seneka bla bla bla
    LETTER XXXI
    More text from Seneka.
"""

# Call the function and print the result
letters_and_texts = split_text_by_letter(test_text)

for letter, text in letters_and_texts.items():
    print("HEY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(f"{letter}:")
    print(text)


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
    letters = split_text_by_letter(text)
    return render(request, 'books/seneka/pg1.html', {'letters': letters})
