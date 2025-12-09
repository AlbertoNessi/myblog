from django.shortcuts import render
from .models import Books, Quotes


def index(request):
    return render(request, 'blog/home.html', {})


def now(request):
    return render(request, 'blog/now.html', {})


def reading(request):
    books = Books.objects.all().order_by('-id')
    return render(request, 'blog/reading.html', {'books': books})


def quotes(request):
    quotes = Quotes.objects.all().order_by('-id')
    return render(request, 'blog/quotes.html', {'quotes': quotes})
