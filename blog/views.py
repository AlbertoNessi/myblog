from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from .models import Books, ProfileContent, Quotes


def llms_txt(request):
    content = (settings.BASE_DIR / "llms.txt").read_text(encoding="utf-8")

    return HttpResponse(content, content_type="text/plain; charset=utf-8")


def index(request):
    profile = ProfileContent.objects.get(pk=1)
    return render(request, 'blog/home.html', {'profile': profile})


def now(request):
    return render(request, 'blog/now.html', {})


def reading(request):
    books = Books.objects.all().order_by('-id')
    return render(request, 'blog/reading.html', {'books': books})


def quotes(request):
    quotesDesc = Quotes.objects.all().order_by('-id')
    return render(request, 'blog/quotes.html', {'quotesDesc': quotesDesc})
