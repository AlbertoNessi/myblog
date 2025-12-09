from django.contrib import admin
from .models import Quotes
from .models import Books

# The ModelAdmin class is the representation of a model in the admin interface

class quotesAdmin(admin.ModelAdmin):
    fields = ['title', 'subtitle', 'date', 'text', 'link', 'author']


class booksAdmin(admin.ModelAdmin):
    fields = ['title', 'subtitle', 'link', 'author']


admin.site.register(Quotes, quotesAdmin)
admin.site.register(Books, booksAdmin)
