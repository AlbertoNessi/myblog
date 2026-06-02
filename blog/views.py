from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from .models import Books, Quotes


def llms_txt(request):
    content = (settings.BASE_DIR / "llms.txt").read_text(encoding="utf-8")

    return HttpResponse(content, content_type="text/plain; charset=utf-8")


def index(request):
    latest_book = Books.objects.all().order_by('-id').first()
    latest_quote = Quotes.objects.all().order_by('-id').first()

    context = {
        'welcome_text': "I'm Alberto Nessi and I'm a web developer based near Milan. "
		"Here to share just what I'm doing now, what I'm reading, watching and some interesting quotes.",
        'now_updates': [
            'Working at Sec Group Srl building B2B web applications.',
            'Studying Python and Django in my free time and experimenting with LLMs too.',
        ],
        'latest_book': latest_book,
        'latest_quote': latest_quote,
    }
    return render(request, 'blog/home.html', context)


def now(request):
    return render(request, 'blog/now.html', {})


def reading(request):
    books = Books.objects.all().order_by('-id')
    return render(request, 'blog/reading.html', {'books': books})


def quotes(request):
    quotesDesc = Quotes.objects.all().order_by('-id')
    quotesAsc = Quotes.objects.all().order_by('id')

    return render(request, 'blog/quotes.html', {'quotesDesc': quotesDesc, 'quotesAsc': quotesAsc})
