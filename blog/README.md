# Blog layout

All public sections use `templates/blog/section_layout.html` and
`static/blog/css/style.css`.

On desktop (above 900px), the navigation and content use one centered grid.
The grid width is 92% of the viewport, with a maximum width of 1020px.
The sidebar uses 220px, including its right padding. The content uses the
remaining width, up to 800px. This keeps the menu close to the text without
making the text column wider.
Automatic side margins center the grid. Keep the content in its grid column;
a horizontal transform moves it away from the centered layout.

Only the content column scrolls. The sidebar and footer stay in place.
The social links align with the bottom of the content box. They stay in
place when the content scrolls.
The desktop sidebar has a known limit in wide, short windows. At 915 by 412
pixels, the contact links overlap the navigation. This size needs a separate
responsive layout change.
On mobile (up to 900px), all four pages use one column and document scrolling.
The page fills the visible viewport, including changes to the browser toolbar.
The content row fills unused vertical space, so the four contact links sit at
the bottom of short pages. On long pages, the links follow all content and
appear when the reader scrolls to the end. They do not cover the content.
The Profile page has an extra row for its portrait. Keep its content row
flexible too. Bottom padding includes the device safe area.

On mobile, `html` and `body` use `overscroll-behavior-y: auto`. This allows
the browser's native bounce at the top and bottom of the document and its
pull-to-refresh gesture where supported. The browser controls the animation
and refresh indicator. The site does not add a custom loading animation.
Desktop keeps its separate content scrolling rules.

The mobile Profile portrait grows while one finger pulls down at the page top.
The Profile-only `profile_portrait.js` measures finger movement with passive
touch events. It does not depend on negative scroll offsets: Safari can keep
the document at 0 while its refresh indicator is visible. Each 40px of pull
adds 10%, up to 15%. A gesture that starts below the top must first use its
initial scroll distance before it can enlarge the portrait.
Updates use at most one pending animation frame. There is no polling loop or
CSS transition while the finger moves. A frame is requested only when the
visible scale changes. Normal scrolling and continued pulls at the 15% limit
do not request more frames. On release, a pull of at least 8px
starts a 340ms rebound: the photo grows by 4% to 15%, briefly contracts by
1.5%, and returns to its normal size. The final touch position is used even
when the gesture ends before the next frame. This keeps fast pulls visible.
Safari's negative scroll offsets also trigger one rebound when momentum
reaches the page top after release. Scroll events do not restart a running
rebound. There is at most one return animation and one pending touch frame.
A new touch cancels the return animation. Cancellation, page restore, layout
changes, and Reduce Motion clear pending work before it can restore an old scale.
The image keeps its proportions and grows from its center. Its layout size
stays fixed, so the text does not move. Normal scrolling and the bottom-edge
bounce do not enlarge it.
The effect is off above 900px and when Reduce Motion is enabled. Multi-touch
gestures clear the effect and keep pinch zoom available.
No touch gesture is cancelled; native scrolling and pull-to-refresh stay active.
The rebound uses the browser's [Web Animations API](https://developer.mozilla.org/en-US/docs/Web/API/Element/animate).
See the [WebKit passive event guidance](https://webkit.org/blog/8216/new-webkit-features-in-safari-11-1/#passive-event-listeners)
for the scrolling behavior of these listeners.

## Colors and footer

All public pages use a fixed light grey background (`#F2F3F4`).
Text, navigation, social links, and content links use petrol blue (`#015B7E`).
The shared CSS defines these colors with `--bg`, `--fg`, and `--link`.
The palette stays the same at all times of day.

The page background has no cloud image. The footer has no illustration.
It shows the copyright in the page font and text color, with 16px padding.
The footer does not load a separate web font.

## CV

The CV button on each public page opens `static/blog/Alberto_Nessi_CV_2026.pdf`
in a new tab. This file contains the current 2026 CV. To update the CV,
replace this PDF and keep its filename so the shared link stays valid.
Local development serves the app's static file. Run `collectstatic` as part
of deployment to update the published copy.

## Images

The nine shared images in `static/blog/images/` use optimized RGBA PNG files.
The portrait is 768 pixels wide. Social and CV icons fit within 144 × 144
pixels. Navigation icons fit within 96 × 96 pixels. Transparency and image
proportions are preserved. CSS sets the display size, so smaller source files
do not make the images smaller on the page. The shared files total about 676 KB.

When replacing an image, resize it for its display size and allow for Retina
screens. Keep the original artwork outside the published static directory.
Set the template's width and height to the new file dimensions and update its
`v` query value so browsers fetch the new image. Run `collectstatic` during
deployment to publish the optimized files.

## Reading book covers

Each book has one visible Link. The title is plain bold text. The link's
click area covers the whole card, including its cover, author, and padding,
on desktop and mobile. It opens the book's existing URL in a new tab.
Tab focuses the single link for each book, and Enter opens it. A visible
outline marks the focused card. The accessible link name identifies the
book and states that it opens a new tab. This uses a native link and CSS;
JavaScript is not required. A book without a URL has no active link area.

In `/admin/`, open Books and select a book, including any existing book.
Use Cover to select a JPEG, PNG, or WebP file, then save. Reopen the book to
see the saved cover preview. Select another file to replace it, or select
Clear and save to remove the cover from the page.

The upload must be a complete still image no larger than 5 MB
(5,242,880 bytes) and no more than 20 million pixels. The admin form validates
the decoded image before storage. It applies the image orientation, keeps its
proportions, and reduces it to fit within 600 by 900 pixels without enlargement.
Transparent areas become white. The saved file is a JPEG with no source
metadata. Its name uses up to 45 characters from the book title, followed by
`--`, a unique 32-character identifier, and `.jpg`. For example:
`the-dream-machine--8f3a91c24e6b49eda04cb239a65629da.jpg`.
The title part keeps letters from other languages and replaces spaces with
hyphens. A title with no usable filename characters uses `book`. The uploaded
filename is not used. The original file on your computer is not changed.

The responsive directory uses the same readable name. Changing only the book
title does not rename files. A new upload uses the current title and a new
identifier, so replacements have new URLs. Existing files keep their names
until the cover is replaced.

Reading shows each cover beside its book details at 100px wide on desktop
and 72px wide on mobile. At 380px and below, the cover sits above the details
so long titles have enough room. The full cover remains visible without cropping.
The page uses `srcset` and `sizes` so the browser can select a file for the
display width and screen density. Widths are 72, 100, 144, 200, 216, and 300
pixels, up to the saved source width. These cover desktop and mobile screens
at densities up to 3x. Small sources are never enlarged. HTML dimensions
reserve space for the image before it loads.

Each book stores `cover_width` and `cover_height` for its saved source JPEG.
The service reads these dimensions while it prepares the responsive files.
It saves the path and dimensions together. Reading uses these database values
for HTML dimensions and responsive widths; it does not open image files or
check storage for each page request. Variant dimensions are calculated from
the source proportions and the fixed widths. They need no database fields.
The image files, URLs, display sizes, and browser selection stay the same.

The book admin shows Cover width and Cover height below the cover preview,
in pixels and as read-only values. An empty cover shows a dash for each value.
Replacing a cover updates both values. Clear sets both to null. A database
constraint requires positive width and height for a nonempty cover path, and
null dimensions for an empty path. A text-only edit keeps the current path and dimensions together,
including after another administrator replaces or clears the cover.

Migration 0007 fills dimensions for existing covers before it adds the
constraint. It reads each source and leaves the source and responsive files
unchanged. Missing or unreadable sources stop the migration. Restore those
files and retry; no request-time fallback reads or guesses dimensions.
See the main README for deployment order and backup requirements.

The admin prepares these JPEG files before it saves a new cover reference.
They are stored below `books/covers/responsive-v1/`, beside the saved sources.
To prepare covers uploaded before this feature, run:

```bash
.venv/bin/python manage.py prepare_book_covers
```

Run this command before serving the updated Reading template in each
environment. It creates missing sizes and leaves source files and database
records unchanged. It can be run again. Page requests do not create files.
Keep the template's `sizes` value and the service widths in step with the
desktop and mobile `.book-cover` CSS widths.

Books keep their text while their covers are being added. A missing cover
does not produce a broken image or an empty reserved column.

Cover editing uses Django admin permissions and CSRF protection. New cover
writes use `BookAdminForm` and `BookCoverService`; future import tools must
use the same validation, conversion, and variant preparation before saving
new cover references and dimensions. Direct ORM writes must also satisfy
the dimension constraint; they do not validate image bytes or prepare sizes.
The database stores a relative file path and the source width and height;
image files are stored below `MEDIA_ROOT/books/covers/`.

Locally, `MEDIA_ROOT` defaults to the ignored `media/` directory. Override it
with `DJANGO_MEDIA_ROOT` when needed. See the main README for production
media serving and backups. After Replacement or Clear is committed to the
database, the old source and its responsive files are removed if no other
book uses that source. An invalid form or a rolled-back edit keeps the old
cover. A text-only edit keeps the latest database cover, including a cover
that another administrator has just replaced.

If old files cannot be removed, the new book data stays saved and the admin
shows a warning that storage maintenance is required. Such failures are
logged. Files left by failed uploads or older versions of the application
are not removed by a broad cleanup. Review and back up those files before
removing them separately. Deleting a book record does not run cover cleanup.

## Favicon and mobile icons

All public pages load the site icons from `static/blog/icons/` through the
shared `base.html` template. The files are resized copies of Alberto's favicon
artwork. The original personal file is not changed.

- `favicon-32x32.png`: transparent 32 × 32 browser icon.
- `favicon.ico`: transparent browser icons at 16 × 16, 32 × 32, and 48 × 48.
- `apple-touch-icon.png`: 180 × 180 icon for iPhone and iPad Home screens.
- `android-chrome-192x192.png` and `android-chrome-512x512.png`: Android icons.
- `site.webmanifest`: site name, Home URL, and Android icon references.

Mobile Home screen icons use the site's light grey background (`#F2F3F4`).
The manifest keeps normal browser navigation with `display: browser`.
When replacing the artwork, regenerate every size from the source image and
update the `v` query values in both `base.html` and `site.webmanifest`.
Run `collectstatic` during deployment to publish these files.

Icon sizes follow the [Apple touch icon guidance](https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/SafariWebContent/ConfiguringWebApplications/ConfiguringWebApplications.html)
and the [Chrome manifest guidance](https://web.dev/articles/add-manifest).
