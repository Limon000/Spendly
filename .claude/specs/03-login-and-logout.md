# Spec: Login and Logout

## Overview
This step adds session-based authentication to Spendly. A registered user
submits their email and password; the app verifies the credentials, stores the
user's id and username in Flask's signed session cookie, and redirects them to
their profile page. A "Sign out" link clears the session and redirects back to
the landing page. After this step the navbar dynamically shows either
"Sign in / Get started" (logged-out) or the username + "Sign out" (logged-in).

## Depends on
- Step 01 — Database Setup (users table must exist)
- Step 02 — Registration (users must be able to create accounts with hashed passwords)

## Routes
- `GET  /login`  — render login form — public
- `POST /login`  — verify credentials, set session, redirect to `/profile` — public
- `GET  /logout` — clear session, redirect to `/` — logged-in (no hard guard yet; safe to call either way)

## Database changes
No new tables or columns.

Add a helper function `get_user_by_email(email)` to `database/db.py` that
returns a single `sqlite3.Row` or `None`.

## Templates
- **Modify:** `templates/login.html`
  - No structural changes needed — form already POSTs to `/login` and renders
    `{{ error }}`. No edits required unless a visual change is desired.
- **Modify:** `templates/base.html`
  - The navbar currently always shows "Sign in" and "Get started".
  - Change the `nav-links` block to branch on `session.get('user_id')`:
    - **Logged-out:** keep current links (Sign in + Get started)
    - **Logged-in:** show username (non-clickable or link to `/profile`) and a
      "Sign out" link pointing to `url_for('logout')`

## Files to change
- `app.py` — add `session` + `check_password_hash` imports; change `/login`
  to GET+POST; implement `/logout`
- `database/db.py` — add `get_user_by_email(email)` helper
- `templates/base.html` — conditional navbar links based on session state

## Files to create
No new files.

## New dependencies
No new dependencies. `werkzeug` is already installed with Flask.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords verified with `werkzeug.security.check_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Session keys to store on login: `session['user_id']` (int) and
  `session['username']` (str)
- Logout must call `session.clear()` — do not pop keys individually
- On failed login show a **generic** error: "Invalid email or password." —
  never reveal which field was wrong (security best practice)
- Redirect after successful login goes to `url_for('profile')` (the existing
  placeholder route is fine for now — Step 04 will flesh it out)
- Redirect after logout goes to `url_for('landing')`

## Definition of done
- [ ] `GET /login` renders the form with no errors
- [ ] Submitting wrong email or non-existent account shows "Invalid email or password."
- [ ] Submitting correct email but wrong password shows the same generic error
- [ ] Submitting valid credentials redirects to `/profile`
- [ ] After login, the navbar shows the logged-in user's username and a "Sign out" link
      instead of "Sign in" / "Get started"
- [ ] Clicking "Sign out" redirects to the landing page `/`
- [ ] After logout, the navbar reverts to the logged-out state
- [ ] Visiting `/login` while already logged in still works (no crash)
- [ ] No 500 errors in any of the above flows
