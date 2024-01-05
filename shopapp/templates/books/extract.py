import PyPDF2

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



from django.shortcuts import render
# (Include the above functions here)

def pdf_view(request):
    pdf_path = 'path/to/your/file.pdf'  # Replace with your PDF file path
    text = extract_text_from_pdf(pdf_path)
    pages = list(split_text_into_chunks(text, 1000))
    return render(request, 'your_template.html', {'pages': pages})
