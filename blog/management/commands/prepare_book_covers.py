from django.core.management.base import BaseCommand

from blog.models import Books
from blog.services import BookCoverService


class Command(BaseCommand):
    help = "Create missing responsive book covers without changing source files or book records."

    def handle(self, *args, **options):
        count = 0
        for book in Books.objects.exclude(cover="").iterator():
            BookCoverService.build_variants(book.cover)
            count += 1
        self.stdout.write(self.style.SUCCESS(f"Prepared responsive covers for {count} books."))
