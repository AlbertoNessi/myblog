# myBlog

Personal Django website project.

## Time-based theme mode

The default theme mode is now set by the visitor's local time:

- `00:00` to `10:00` -> `dark`
- `10:01` to `18:00` -> `light`
- `18:01` to `23:59` -> `dark`

Implementation: `blog/static/blog/js/change_colors.js`

Notes:

- The default mode is recalculated on each page load.
- The theme toggle button still works manually during the current page session.

## Verification

Checks run after implementation:

- Boundary-time runtime checks in Node (no dependencies): `00:00`, `10:00`, `10:01`, `18:00`, `18:01`, `23:59`
- Django project check: `./.venv/bin/python manage.py check`
