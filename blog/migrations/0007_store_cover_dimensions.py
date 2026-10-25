from django.db import migrations, models
from PIL import Image


def store_cover_dimensions(apps, schema_editor):
    """Read existing sources and store their dimensions. Fail on unreadable files."""
    Books = apps.get_model("blog", "Books")
    database = schema_editor.connection.alias
    books = Books.objects.using(database).exclude(cover="").select_for_update()
    for book in books.iterator():
        with book.cover.storage.open(book.cover.name, "rb") as source:
            with Image.open(source) as image:
                width, height = image.size
        Books.objects.using(database).filter(pk=book.pk).update(
            cover_width=width,
            cover_height=height,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0006_book_cover_dimensions"),
    ]

    operations = [
        # Separate column creation so a failed file read can be retried on MySQL.
        migrations.RunPython(store_cover_dimensions, migrations.RunPython.noop, atomic=True),
        migrations.AddConstraint(
            model_name='books',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('cover', ''), ('cover_height__isnull', True), ('cover_width__isnull', True)), models.Q(models.Q(('cover', ''), _negated=True), ('cover_height__gt', 0), ('cover_height__isnull', False), ('cover_width__gt', 0), ('cover_width__isnull', False)), _connector='OR'), name='book_cover_dimensions_match'),
        ),
    ]
