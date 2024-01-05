import re
import PyPDF2
from django.shortcuts import render
import os
from django.conf import settings

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
    # pattern = r'(LETTER\s+[IVXLCDM]+\s+[IVXLCDM]*)'
    # pattern = r'(LETTER (?:X{0,3}(?:IX|IV|V?I{0,3})|IX|IV|V?I{0,3}))'
    # pattern = r'(LETTER\s+(?:[IVXLCDM]+\s*)+)'
    parts = re.split(pattern, text)
    letters_dict = {}
    if parts:
        if parts[0] == '':
            parts.pop(0)
        if parts[0] == ' LETTERS  \n \n \n ':
            parts.pop(0)
        for i in range(0, len(parts) - 1, 2):
            heading = parts[i]
            content = parts[i+1] if i + 1 < len(parts) else ""
            letters_dict[content] = heading
    print(letters_dict.keys())
    return letters_dict


# Test the function with some text
test_text = """
    LETTER LXXXVIII
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



pdf_path = os.path.join(settings.BASE_DIR, 'shopapp/views/letters-from-a-stoic_lucius-annaeus-seneca.pdf')
text = extract_text_from_pdf(pdf_path)
letters = split_text_by_letter(text)


def pdf_view(request):
    return render(request, 'books/seneka/pg1.html', {'letters': letters})


def letter_view(request, letter_id):
    length = len(letters)
    heading = ""
    previous_id = 1
    next_id = length

    try:
        int_letter_id = int(letter_id)
        if int_letter_id in range(1, length):
            content, heading = list(letters.items())[int_letter_id-1]
            previous_id = int_letter_id - 1 if int_letter_id > 1 else 1
            next_id = int_letter_id + 1 if int_letter_id < length else length
        else:
            content = "Letter not found"
    except Exception as e:
        content = "Letter not found"
    context = {
        'letter': letter_id,
        'text': content,
        'heading': heading,
        "previous": previous_id,
        "next": next_id,
        "length": str(length-1)
    }

    return render(request, 'books/seneka/letter.html', context=context)
