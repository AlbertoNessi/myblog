from django.shortcuts import render


def index(request):	
    return render(request, 'blog/home.html', {})


def now(request):
    return render(request, 'blog/now.html', {})


def reading(request):
    return render(request, 'blog/reading.html', {})


def quotes(request):
    return render(request, 'blog/quotes.html', {})
