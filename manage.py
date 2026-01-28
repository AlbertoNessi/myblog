#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""

    # Load local environment variables BEFORE Django imports settings.
    # This prevents KeyError for vars like DJANGO_SECRET_KEY / DB_PASSWORD
    # when running manage.py commands locally.
    try:
        from dotenv import load_dotenv

        # Keep the file local-only (gitignored). In production you should
        # rely on real environment variables from systemd/Docker/etc.
        load_dotenv(".env.local")
    except Exception:
        # If python-dotenv isn't installed, we keep going and let Django
        # use whatever environment variables are already present.
        pass

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myBlog.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
