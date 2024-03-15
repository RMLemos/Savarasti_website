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


def author(request, slug):
    authors = Author.objects.get(slug=slug)
    books = Book.objects.filter(
        author=author,
    ).order_by('-id')

    context = {
        'books': books,
        'author': authors,
    }

    return render(request, 'library/author.html', context)

def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    author_books = Book.objects.filter(author__in=book.author.all()).exclude(id=book.id).distinct()
    context = {
        'book': book,
        'author_books': author_books,
    }

    return render(request, 'library/single-book.html', context)