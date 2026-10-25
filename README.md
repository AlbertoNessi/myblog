# myBlog

Personal Django website project.

See [Blog layout, colors, CV, and images](blog/README.md) for the shared page
layout, desktop centering, sidebar spacing, mobile footer placement, CV updates,
native mobile scrolling, the Profile portrait pull and rebound with updates only
when its scale changes, image size limits,
responsive book cover uploads, clickable Reading cards, and favicon and mobile
icon configuration.

See [Cover storage design](DESIGN.md) for cover validation, file storage,
stored cover dimensions with read-only admin values, readable filenames,
replacement cleanup, and failure behavior.

All public pages use a fixed light grey background (`#F2F3F4`) and petrol
blue text and links (`#015B7E`). The background and footer have no
illustrations. The palette does not change with the visitor's local time.

## Local development and iPhone preview

Install the project dependencies, including Pillow for book covers:

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py migrate
```

Start the development server from the project directory:

```bash
.venv/bin/python manage.py runserver 0.0.0.0:8000
```

Local settings are loaded from `.env.local`. With `DJANGO_DEBUG=1`, Django
also accepts the Mac's current Wi-Fi address, `192.168.1.2`. This address is
not added to the allowed hosts when debug mode is off.

Connect the iPhone to the same Wi-Fi network and open
`http://192.168.1.2:8000/` in Safari. The Mac can also use
`http://127.0.0.1:8000/`. If the router changes the Mac's IP address, update
the development address in `myBlog/settings.py` and use the new URL.

## Uploaded book covers in production

Before deploying the cover feature, install `requirements.txt`, inspect
`python manage.py sqlmigrate blog 0005`, then apply the migration.
Run `collectstatic` to publish the updated layout.
Before serving the responsive Reading template, run
`python manage.py prepare_book_covers` to prepare the existing covers. Include
the generated media files in backups. See the blog README for image sizes.

For stored cover dimensions, back up the database and media, stop application
workers and cover edits, and inspect `python manage.py sqlmigrate blog 0006`
and `python manage.py sqlmigrate blog 0007`. Then run
`python manage.py migrate blog` before starting the updated application.
Migration 0006 adds two columns. Migration 0007 reads each existing source,
stores its width and height, and adds the cover dimension constraint. It needs
the existing media directory at the configured `DJANGO_MEDIA_ROOT`.
If a source is missing or unreadable, restore that source and retry the
migration. The application does not guess dimensions or regenerate images.
See the blog README for the dimension rules and the design file for the
migration failure behavior.

Set `DJANGO_MEDIA_ROOT` to a persistent directory that the Django process can
write to. The default production directory is `/var/www/myblog/media/`.
Configure the web server to serve `/media/` from this same directory. For
example, an Nginx server block can use the following settings. The request
limit leaves room for a 5 MB image and the other form fields:

```nginx
client_max_body_size 6m;

location /media/ {
    alias /var/www/myblog/media/;
}
```

Use the configured path in the alias if `DJANGO_MEDIA_ROOT` is changed.
Keep media outside release directories. With containers, mount persistent
storage at that path. Back up the media directory together with the database.
Uploaded files are separate from static files and are not part of
`collectstatic`. Django serves media directly only in local debug mode.

See [Reading cover usage and limits](blog/README.md#reading-book-covers)
for the admin workflow, supported files, and replacement behavior.
