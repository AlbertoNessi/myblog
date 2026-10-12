from django.contrib import admin
from .models import Books, ProfileContent, Quotes

# The ModelAdmin class is the representation of a model in the admin interface

class quotesAdmin(admin.ModelAdmin):
    fields = ['title', 'subtitle', 'date', 'text', 'link', 'author']


class booksAdmin(admin.ModelAdmin):
    fields = ['title', 'subtitle', 'link', 'author']


class ProfileContentAdmin(admin.ModelAdmin):
    fields = ['introduction', 'body']

    def render_change_form(self, request, context, add=False, change=False, form_url="", obj=None):
        context["show_save_and_add_another"] = False
        return super().render_change_form(request, context, add, change, form_url, obj)

    def has_add_permission(self, request):
        return super().has_add_permission(request) and not ProfileContent.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Quotes, quotesAdmin)
admin.site.register(Books, booksAdmin)
admin.site.register(ProfileContent, ProfileContentAdmin)
