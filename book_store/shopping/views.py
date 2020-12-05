from django.shortcuts import render
from .models import Book


# Create your views here.
def main(request):
    book = Book()
    context = {
        'object': book
    }
    return render(request, 'shopping/start_rating_test.html', context)
