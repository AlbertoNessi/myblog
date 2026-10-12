from django.db import models


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

    def __str__(self):
        return self.title
