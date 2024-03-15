from django.shortcuts import get_object_or_404, render

from library.models import Author, Book

app_name = 'library'

def index(request):
    author = Author.objects.order_by('name')
    books = Book.objects.order_by('-id')

    context = {
        'authors': author,
        'books': books,
    }
    return render(request, 'library/index.html', context)