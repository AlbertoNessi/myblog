from django.db import models

from .services import BookCoverService


class ProfileContent(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)
    introduction = models.TextField()
    body = models.TextField()

    class Meta:
        verbose_name = "Profile content"
        verbose_name_plural = "Profile content"
        constraints = [
            models.CheckConstraint(condition=models.Q(id=1), name="profile_content_single_row"),
        ]

    def __str__(self):
        return "Profile"


class Quotes(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField('publishing date')
    text = models.TextField()
    link = models.CharField(max_length=200)
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Books(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=100, null=True, blank=True)
    link = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    cover = models.ImageField(
        upload_to="books/covers/",
        blank=True,
        help_text="Upload a JPEG, PNG, or WebP image, up to 5 MB and 20 million pixels.",
    )
    cover_width = models.PositiveIntegerField(null=True, editable=False)
    cover_height = models.PositiveIntegerField(null=True, editable=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(cover="", cover_width__isnull=True, cover_height__isnull=True)
                    | (
                        ~models.Q(cover="")
                        & models.Q(
                            cover_width__isnull=False,
                            cover_height__isnull=False,
                            cover_width__gt=0,
                            cover_height__gt=0,
                        )
                    )
                ),
                name="book_cover_dimensions_match",
            ),
        ]

    def __str__(self):
        return self.title

    @property
    def cover_image(self):
        if self.cover:
            return BookCoverService.image_sources(self.cover, self.cover_width, self.cover_height)
        return None
