from io import BytesIO
from pathlib import PurePosixPath

from django.core.files.base import ContentFile
from django.db import router
from PIL import Image


class BookCoverService:
    """Prepare cover sizes before a book is saved and describe them for HTML."""

    # Keep these widths sufficient for the CSS sizes at densities up to 3x.
    WIDTHS = (72, 100, 144, 200, 216, 300)

    @classmethod
    def widths_for(cls, source_width):
        return sorted({min(width, source_width) for width in cls.WIDTHS})

    @staticmethod
    def variant_directory(cover):
        source = PurePosixPath(cover.name)
        # Use a new directory version if the image conversion rules change.
        return str(source.parent / "responsive-v1" / source.stem)

    @classmethod
    def variant_name(cls, cover, width):
        return str(PurePosixPath(cls.variant_directory(cover)) / f"{width}.jpg")

    @classmethod
    def prepare_upload(cls, book, cover_changed):
        """Lock the current row and prepare a valid admin edit inside a transaction.

        Return the previous cover only when it must be removed after commit.
        Keep the current database cover when the form does not change it.
        """
        previous_cover = None
        if book.pk:
            database = router.db_for_write(type(book), instance=book)
            previous = type(book).objects.using(database).select_for_update().get(pk=book.pk)
            previous_cover = previous.cover
            if not cover_changed:
                # A concurrent replacement must not be undone by a text edit.
                book.cover = previous_cover.name
                book.cover_width = previous.cover_width
                book.cover_height = previous.cover_height
                return None

        cover = book.cover
        if cover and not cover._committed:
            cover.save(cover.name, cover.file, save=False)
            book.cover_width, book.cover_height = cls.build_variants(cover)
        elif not cover:
            book.cover_width = None
            book.cover_height = None

        if previous_cover and previous_cover.name != cover.name:
            return previous_cover
        return None

    @classmethod
    def delete_unused_cover(cls, cover):
        """Remove an unused source and its sizes. Storage failures remain visible."""
        books = type(cover.instance).objects.using(cover.instance._state.db)
        if books.filter(cover=cover.name).exists():
            return

        directory = cls.variant_directory(cover)
        try:
            _, files = cover.storage.listdir(directory)
        except FileNotFoundError:
            # A repeated cleanup can find that the sizes are already removed.
            files = []
        for filename in files:
            cover.storage.delete(str(PurePosixPath(directory) / filename))
        # FieldFile.delete() can save the old book data. Delete storage files only.
        cover.storage.delete(cover.name)

    @classmethod
    def build_variants(cls, cover):
        """Create missing sizes and return the source dimensions. Keep the source."""
        with cover.storage.open(cover.name, "rb") as source:
            with Image.open(source) as image:
                widths = cls.widths_for(image.width)
                for width in widths:
                    name = cls.variant_name(cover, width)
                    if cover.storage.exists(name):
                        continue
                    height = max(1, round(image.height * width / image.width))
                    resized = image.resize((width, height), Image.Resampling.LANCZOS)
                    output = BytesIO()
                    resized.save(output, format="JPEG", quality=85, optimize=True)
                    cover.storage.save(name, ContentFile(output.getvalue()))
                return image.size

    @classmethod
    def image_sources(cls, cover, width, height):
        """Describe prepared sizes with stored dimensions. Do not open image files."""
        widths = cls.widths_for(width)
        sources = []
        for candidate in widths:
            url = cover.storage.url(cls.variant_name(cover, candidate))
            sources.append(f"{url} {candidate}w")
        return {
            "url": cover.storage.url(cls.variant_name(cover, min(100, width))),
            "srcset": ", ".join(sources),
            "width": width,
            "height": height,
        }
