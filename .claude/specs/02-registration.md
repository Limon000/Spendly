# Spec: Registration

## Overview
This step implements user registration for Spendly. A visitor fills in their
name, email, and password; the app validates the input, hashes the password,
inserts the new user into the `users` table, and redirects to the login page.
This is the first step that writes data to the database and requires Flask's
secret key for flash messages.

## Depends on
- Step 01 — Database Setup (users table must exist)

## Routes
- `GET  /register` — render the registration form — public
- `POST /register` — process form submission, create user, redirect to login — public

## Database changes
No new tables or columns. The existing `users` table already has all required
fields: `id`, `username`, `email`, `password_hash`, `created_at`.

Add a helper function `create_user(username, email, password_hash)` to
`database/db.py`.

## Templates
- **Modify:** `templates/register.html`
  - The form field `name` maps to `username` in the database — confirm the
    `name` attribute on the input is `username` (currently it is `name`; update
    to `username` so form data matches the DB column)
  - The template already renders `{{ error }}` — no structural changes needed
    beyond the field rename

## Files to change
- `app.py` — add `app.secret_key`, accept POST on `/register`, add import for
  `werkzeug.security.generate_password_hash`, add import for `redirect`,
  `url_for`, `request` from flask, wire up registration logic
- `database/db.py` — add `create_user` helper
- `templates/register.html` — rename input `name="name"` → `name="username"`

## Files to create
No new files.

## New dependencies
No new dependencies. `werkzeug` is already installed with Flask.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with `werkzeug.security.generate_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Set `app.secret_key` to a hard-coded dev string (e.g. `"dev-secret-key"`) —
  note in a comment that this must be replaced with an env var before production
- Validate in this order, re-rendering the form with an `error` variable on failure:
  1. All fields present and non-empty
  2. Password is at least 8 characters
  3. Email not already registered (catch `sqlite3.IntegrityError` or pre-check)
  4. Username not already taken (same)
- On success: redirect to `url_for('login')` — do NOT log the user in yet
  (login is Step 3)

## Definition of done
- [ ] Visiting `GET /register` renders the form with no errors
- [ ] Submitting empty fields re-renders the form with an error message
- [ ] Submitting a password shorter than 8 characters shows an error
- [ ] Submitting a duplicate email shows "Email already registered" (or similar)
- [ ] Submitting a duplicate username shows "Username already taken" (or similar)
- [ ] Submitting valid unique data inserts a row into `users` with a hashed
      password (verify via `sqlite3` CLI or DB browser — the stored value must
      NOT be the plain-text password)
- [ ] After successful registration the browser is redirected to `/login`
- [ ] The `/login` page is reachable after registration (no 500 errors)
