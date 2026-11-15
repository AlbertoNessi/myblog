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
On Quotes, only the quote list scrolls; the search panel stays above it.
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

The mobile contact footer uses 12px of top padding and 12px of page bottom
padding, plus the device safe area. Each icon stays in a 48 by 48px box.
The gap between each icon and its label is 4px. Labels keep their 11px font,
and each link keeps its minimum height of 64px. These rules apply to all
four public pages up to 900px. Desktop spacing is separate.

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

## Mobile navigation

The head sets a `js` class on the root element before CSS loads. Up to 900px,
this class shows the menu button and keeps the closed menu outside the page
flow from the first paint. The page content does not move when the deferred
navigation script starts. The script sets the closed state before it adds
`has-menu`. Mouse, touch, Space, Escape, and outside clicks keep the existing
behavior. Desktop keeps its visible sidebar navigation.

With JavaScript disabled, the button stays hidden and the navigation links
stay visible in the page flow. If the navigation script cannot load, its
error handler removes `js` and restores these same links.

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

The portrait uses six lossless WebP files in `static/blog/images/`, with widths
of 144, 216, 320, 512, 640, and 768 pixels. The original RGBA PNG is kept as
the source. The 768px WebP has the same decoded pixels as this source.
Smaller files use Lanczos resizing and lossless encoding, with transparency
and proportions preserved. Their sizes range from about 23 KB to 402 KB,
compared with the 567 KB source. The browser downloads one suitable candidate,
not the full set.

`includes/profile_portrait.html` keeps the original image ID, alt text, and
768 by 869 HTML dimensions. The Home include passes `large_portrait=True`
to select sizes for the large mobile portrait. Other pages use the 72px
mobile header size. Desktop sizes follow the existing viewport-height rule.
Keep these `sizes` values aligned with the CSS if the layout changes.
The portrait remains eagerly loaded. Its CSS size and appearance do not change.

Social and CV icons keep their optimized RGBA PNG files within 144 by 144
pixels. Navigation icons fit within 96 by 96 pixels. CSS sets their display size.
The shared book mockup described below adds about 130 KiB on desktop and
mobile. All books share the same background file.

When replacing an image, resize it for its display size and allow for Retina
screens. Keep the original artwork outside the published static directory.
Set the template's width and height to the new file dimensions and update its
`v` query value so browsers fetch the new image. Run `collectstatic` during
deployment to publish the optimized files. To replace the portrait, prepare
all six widths from the same source without enlargement, then encode each
resized PNG with `cwebp -lossless -z 9 -exact`. Keep the original source too.

## Opening quotes

Quote subtitles, authors, source links, and quote text use italics.
Titles keep normal bold type. Dates and search controls keep normal type.
The author uses the label "By:" and appears beside the title when both fit.
When space is limited, the author moves below the title. Long titles and
author names wrap within the card. The author stays visible when the quote
is closed and is not repeated in the open body. A quote with no author shows
only its title. The title and author share the native summary control.

Click anywhere in a closed quote card's white hover area to open it, including
the space around the title. The native `summary` contains the card padding,
so its full area opens and closes the quote without JavaScript. Enter and Space
work when the summary has keyboard focus.

An open quote keeps its text and source links separate from this control.
Selecting text or using a source link does not close the quote. Mobile keeps
its full-width summary and existing spacing.

## Quotes search

On `/quotes`, use Search quotes to find part of an author, title, source URL,
or quote text. Search ignores letter case and spaces at the start and end of
the query. Results keep the newest-first order. An empty query or Clear shows
all quotes. No matches shows "No quotes found."

On desktop (above 900px), the search input and icon are visible, and the Clear
link is hidden. Empty the input to restore all quotes. The input aligns to the
right edge of the quote cards. The panel reserves the same scrollbar space as
the list to keep this edge aligned.

On mobile, the search field is at most 280px wide, with a small search icon,
the page font, and petrol blue text. It aligns to the right edge of the quote
cards. Clear appears to the left of the input, so the input's right edge stays
in place. The accessible input name is "Search quotes".

On mobile, the input and Clear have touch areas at least 44px high. Clear has
a reserved 44px column, so the input does not move or shrink when text is entered.
Clear is hidden for an empty query on mobile.
The input keeps its 16px font and right alignment. The sticky panel has 8px of
top padding. The input requests a Search key and disables automatic capitalization,
correction, spelling marks, and saved input suggestions. The browser controls
the keyboard. The touch sizes follow the
[W3C target size guidance](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html).

The search panel is outside the scrolling quote list on desktop. The list can
receive keyboard focus for scrolling. On mobile, the document still scrolls;
the search panel stays at the top while the quote section is visible. Its solid
background keeps the quotes from showing through the search controls.
A fixed background also covers the device's top safe area across the viewport.
It uses the same safe-area height as the sticky panel offset. This stops quote
text from appearing above the search while the document scrolls. It does not
change the input position or initial spacing and does not intercept touch events.
Desktop keeps its existing search layout.

With JavaScript, results update 250 ms after typing stops. Only the quote list
is replaced, so the input keeps focus. A new input cancels the previous request.
Text composition pauses the search until the keyboard commits the text.
Clear empties the field and filters again without a page reload. On mobile,
focus stays in the input. Without JavaScript,
Clear remains a link to the full quote list.
`quotes_search.js` uses the same GET endpoint and `QuoteSearchService` filter;
the search rules stay on the server. The URL keeps the current successful query
in `q`, so it can be bookmarked. Failed requests show an error and keep the last
results visible. Press Enter to submit the form, including when
JavaScript is off. No database changes are required.

## Reading book covers

The title, author, and optional subtitle are centered vertically beside the cover
on desktop.

On desktop (above 900px), Reading shows one book per row with its cover beside
the details. Titles use bold 22px type. The author appears below the title,
and the optional subtitle appears below the author. Both use italics.

On mobile (up to 900px), Reading shows two equal columns of large book covers.
The Reading heading has an 8px bottom margin, 16px less than other sections.
Books use the same 3D frame, cover placement, and shadow as desktop.
The book box is 120px wide below 392px, 160px wide from 392px,
and 240px wide from 552px to 900px. Its 15:22 aspect ratio fits the artwork
and its top inset without extra space below. The title starts 4px below
the artwork canvas. The visible book keeps its size and position.
Each size fits the two-column grid.
Each cell shows the cover above a centered bold 14px title and a smaller
12px italic author. Subtitles are hidden. Titles wrap to at most two lines,
with an ellipsis for longer text and no underline. The full title stays in
the link's accessible name. Author names wrap within the cell without a
line limit. The grid uses 24px column gaps and 28px row gaps.
Books without covers keep their title and author in the same grid.

The title is the book's single link, with no separate "Link" label. The link's
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

Reading places each cover on the same fixed book image. The transparent
`static/blog/images/book-mockup.webp` contains the pages, binding, boards, and
shadow. Its soft 3D style follows the Reading and CV icons. Each book uses a
100 by 160px box on desktop and the sizes listed above on mobile. All books have
the same shape and thickness. They do not rotate or animate.

The cover fills the front face with a central crop. It keeps its proportions;
parts near the edges can be hidden. The uploaded files are not changed.
Books without covers show text only.

The artwork uses a fixed 300 by 400 coordinate space. The CSS matrix maps a
200 by 300 cover to front-face corners (28, 35.8), (259.5, 36.2),
(259.5, 371), and (28, 371), in clockwise order. One scale changes both the
background and cover for each viewport. When replacing the image, keep its 3:4
canvas ratio and update these corners and the matrix together. Keep the narrow
board rim visible. The image is a lossless WebP at 450 by 600 pixels with
transparency. Its decoded pixels match the generated PNG. To convert a new
PNG without changing its pixels or transparent areas, use:

```bash
cwebp -lossless -z 9 -exact book-mockup.png -o book-mockup.webp
```

This conversion is a one-time asset preparation step. The application does
not need an image conversion tool at runtime.

The page uses `srcset` and `sizes` so the browser can select a file for the
display width and screen density. Widths are 72, 100, 144, 200, 216, and 300
pixels, up to the saved source width. When the source is wider than these
variants, it is also an explicit candidate at its stored width. This lets
large mobile covers use the existing source on high-density screens without
new image generation. Detail is limited by the saved source resolution.
Small sources are never enlarged during preparation. HTML dimensions
reserve space for the image before it loads.

Each book stores `cover_width` and `cover_height` for its saved source JPEG.
The service reads these dimensions while it prepares the responsive files.
It saves the path and dimensions together. Reading uses these database values
for HTML dimensions and responsive widths; it does not open image files or
check storage for each page request. Variant dimensions are calculated from
the source proportions and the fixed widths. They need no database fields.
The storage paths and responsive size rules do not depend on the book mockup.

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
desktop and mobile `.book-object` CSS widths. Desktop sizes also cover the
narrower front face of the fixed book image.

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
