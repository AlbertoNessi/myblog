from io import BytesIO
from uuid import uuid4

from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
from django.utils.text import slugify
from PIL import Image, ImageOps

from .models import Books


class BookAdminForm(forms.ModelForm):
    """Validate new cover uploads and produce a small JPEG before storage."""

    class Meta:
        model = Books
        fields = ["title", "subtitle", "link", "author", "cover"]
        widgets = {
            "cover": AdminFileWidget(
                attrs={"accept": "image/jpeg,image/png,image/webp"}
            ),
        }

    def clean_cover(self):
        cover = self.cleaned_data.get("cover")
        if not isinstance(cover, UploadedFile):
            return cover

        if cover.size > 5 * 1024 * 1024:
            raise forms.ValidationError("The cover must be no larger than 5 MB.")

        if cover.image.format not in {"JPEG", "PNG", "WEBP"}:
            raise forms.ValidationError("Use a JPEG, PNG, or WebP image.")

        width, height = cover.image.size
        if width * height > 20_000_000:
            raise forms.ValidationError("The cover must not exceed 20 million pixels.")

        # Decode the full image so truncated files cannot reach storage.
        try:
            with Image.open(cover) as image:
                if getattr(image, "n_frames", 1) != 1:
                    raise forms.ValidationError("Use a still image for the cover.")
                image = ImageOps.exif_transpose(image)
                image.thumbnail((600, 900), Image.Resampling.LANCZOS)
                rgba = image.convert("RGBA")
                background = Image.new("RGB", image.size, "white")
                background.paste(rgba, mask=rgba.getchannel("A"))
                output = BytesIO()
                # A new JPEG removes file metadata and uses a safe file name.
                background.save(output, format="JPEG", quality=85, optimize=True)
        except (OSError, SyntaxError, ValueError) as error:
            raise forms.ValidationError("Upload a complete, valid image.") from error

        # Leave room for the unique suffix within the cover field's path limit.
        title_slug = slugify(self.cleaned_data.get("title", ""), allow_unicode=True)
        title_slug = title_slug[:45].strip("-_")
        if not title_slug:
            title_slug = "book"
        return SimpleUploadedFile(
            f"{title_slug}--{uuid4().hex}.jpg",
            output.getvalue(),
            content_type="image/jpeg",
        )
