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
The mobile layout uses the existing single column rules.

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
