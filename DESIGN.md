# Reading cover storage

The admin form is the entry point for new book cover files. Reading only
displays stored covers. The application does not search external catalogs.

## Data flow and rules

1. An authorized administrator sends a file with the book form.
2. Django validates that the file is an image. `BookAdminForm` checks the
   format, byte count, pixel count, and frame count. It then decodes the full
   image so a truncated file cannot be saved.
3. The form applies orientation and reduces the image to fit within 600 by
   900 pixels. It creates a new JPEG on a white background. Source metadata
   and the source filename are not copied. The new name uses a title slug
   of at most 45 characters and a new UUID. Unicode letters are retained.
   Titles without usable filename characters use `book`. The full path fits
   within the cover field's 100-character limit.
4. For a valid form, the admin calls `BookCoverService` before the database
   write. It saves the JPEG under `books/covers/` and creates responsive sizes
   below `books/covers/responsive-v1/`. During this same image read, it gets
   the final JPEG width and height. The book row stores the source file path
   and these two dimensions in one write. On edits, the service locks the
   current book row before it reads the previous cover. Text-only edits keep
   that current cover and its dimensions, so a stale form cannot restore a
   file removed by a concurrent replacement.
   Existing uploads use the explicit `prepare_book_covers` command.
5. Reading uses the prepared sizes with HTML `srcset` and `sizes`. The
   service uses stored dimensions and makes no image file reads or storage
   existence checks. The browser selects a file for the display width and
   screen density. The admin preview uses the source URL. The web server
   serves the files; Django
   serves them directly only in debug mode.

The accepted formats are JPEG, PNG, and WebP. Files must contain one frame,
at most 5,242,880 bytes, and at most 20 million pixels. Images keep their
proportions and are never enlarged. New writes must pass through the form's
validation, conversion, and responsive size preparation; direct ORM writes
do not validate image contents or prepare sizes. Such writes must supply
accurate source dimensions too. A database constraint requires either an
empty cover path and two null dimensions, or a nonempty path and two positive
dimensions. It rejects missing, partial, and zero dimensions before storage
in the database. The service owns dimension accuracy; clients cannot edit
these values through the admin form.

Responsive widths are 72, 100, 144, 200, 216, and 300 pixels. They cover
72px mobile images and 100px desktop images at densities up to 3x. Smaller
sources cap these widths and duplicate widths are removed. File names and
HTML width descriptors use the actual output width. No image is enlarged
or cropped. The source file is preserved.

Only the source width and height are stored. Variant widths come from the
fixed size list, capped at the source width. Variant heights use the source
aspect ratio and the existing pixel rounding rule. This keeps two metadata
fields per book instead of a separate record for each image file.

The fields are plain numeric columns. They do not use ImageField dimension
hooks that can open files during model construction. Image reads belong to
validated cover preparation and the explicit historical data migration.

File paths depend on the unique source name and the variant version.
Replacement uploads get new paths. The preparation command creates only
missing files and does not change book records. Page requests describe
prepared files; they do not generate images or substitute a large source
when preparation is missing. Run the command before enabling the updated
template for historical uploads in each environment. Missing or unreadable
sources remain visible as errors during preparation.

Editing a title without uploading a cover does not rename existing files.
This avoids a file move during a text edit and preserves working URLs.
Existing UUID-only filenames remain valid until replacement.

The cover field starts empty for existing books so their covers can be added
without changing their other data. An empty cover is an explicit state during
entry or removal. Reading omits the image in that state.

## Dimension migration

Back up the database and media and stop application workers and cover edits
before migrating. Inspect the SQL for migrations 0006 and 0007. Apply both
before starting the updated application with access to the existing media.

Migration 0006 adds the nullable width and height columns. Migration 0007
reads existing sources, locks their rows, writes their actual dimensions in
a transaction, and then adds the dimension constraint. The column migration
is separate because MySQL cannot roll back DDL. If a source read fails, the
dimension writes roll back and 0006 stays applied. Restore the missing or
unreadable source and rerun migration 0007. There are no guessed values and
no fallback reads during page requests. Images are not changed or generated.

## Ownership and failure behavior

The database owns the association between a book and its cover. The media
directory owns the file bytes. It must survive deployments and have a backup
that matches the database backup. `collectstatic` does not manage media.

Invalid uploads produce form errors before storage. A failed form submission
does not replace a saved cover. File system and database failures remain
visible; the application does not report success after an unexpected error.

The admin registers old-file cleanup with `transaction.on_commit`. Cleanup
runs only after the book edit and related admin writes commit. It checks
that no book still refers to the old source, removes the files in that source's
responsive directory, and then removes the source. Clear uses the same path.
Missing files make repeated cleanup safe. Other storage errors remain visible:
the admin logs the error and shows a warning that the book was saved but old
files need maintenance. It does not undo the new committed cover.

File storage does not participate in database transactions. A failed file or
database write can leave new unreferenced files. A storage failure during
cleanup can leave some old files. The trade-off is that automatic cleanup
stops at a confirmed replacement or Clear; it does not scan for or guess
the ownership of older orphaned files. Those need explicit maintenance
after reference checks and backup. Deleting a book record does not trigger
this replacement cleanup.
