from functools import partial
import logging

from django.contrib import admin, messages
from django.db import transaction
from django.utils.html import format_html

from .forms import BookAdminForm
from .models import Books, ProfileContent, Quotes
from .services import BookCoverService

logger = logging.getLogger(__name__)

# The ModelAdmin class is the representation of a model in the admin interface

class quotesAdmin(admin.ModelAdmin):
    fields = ['title', 'subtitle', 'date', 'text', 'link', 'author']


class booksAdmin(admin.ModelAdmin):
    form = BookAdminForm
    fields = ['title', 'subtitle', 'link', 'author', 'cover', 'cover_preview', 'cover_width', 'cover_height']
    readonly_fields = ['cover_preview', 'cover_width', 'cover_height']

    def save_model(self, request, obj, form, change):
        previous_cover = BookCoverService.prepare_upload(obj, "cover" in form.changed_data)
        super().save_model(request, obj, form, change)
        if previous_cover:
            # The admin commits related writes before old files can be removed.
            transaction.on_commit(
                partial(self.remove_previous_cover, request, previous_cover),
                using=obj._state.db,
            )

    def remove_previous_cover(self, request, cover):
        try:
            BookCoverService.delete_unused_cover(cover)
        except OSError:
            logger.exception("Could not remove old cover for book %s", cover.instance.pk)
            self.message_user(
                request,
                "The book was saved, but the old cover files could not be removed. "
                "They need storage maintenance.",
                level=messages.WARNING,
            )

    @admin.display(description="Current cover")
    def cover_preview(self, obj):
        if obj is None or not obj.cover:
            return "No cover uploaded."
        return format_html(
            '<img src="{}" alt="Cover of {}" style="max-width: 120px; max-height: 180px;">',
            obj.cover.url,
            obj.title,
        )


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
