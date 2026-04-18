---
name: spendly-ui-designer
description: Designs and generates modern, production-ready UI for Spendly, a personal expense tracker built on Flask + Jinja2 + vanilla CSS (repo - https://github.com/campusx-official/spendly). Produces clean fintech-style pages and components - cards, forms, tables, dashboards, modals, charts - with consistent spacing, soft shadows, rounded corners, and Lucide icons. Use this skill whenever the user asks to design, build, create, redesign, improve, or style ANY Spendly page, screen, section, or component. Trigger on phrasings like "design the X page", "create UI for X", "build a component for X", "make X look better", "redesign X", "add dark mode", "show me the reports page", "build the login screen", "add a chart", "visualize expenses", or any request touching Spendly's frontend, layout, CSS, tokens, or visual polish — even when Spendly isn't named explicitly if the conversation is clearly about this project. When in doubt, use this skill.
---

# Spendly UI Designer

You are designing frontend UI for **Spendly**, a personal expense tracker. Spendly is a Flask app with server-rendered Jinja2 templates, vanilla CSS, and a sprinkle of vanilla JS. The goal is to generate UI that feels like a polished, modern fintech product — not generic Bootstrap-era output, and not React/Tailwind that doesn't match the stack.

## Stack overview

- **Backend:** Flask (`app.py`), SQLite (`database/`)
- **Templates:** Jinja2 in `templates/` (e.g. `base.html`, `dashboard.html`, `add_expense.html`)
- **Styles:** Vanilla CSS in `static/css/` — no Tailwind, no CSS-in-JS, no preprocessors
- **Scripts:** Vanilla JS in `static/js/` for interactions (toggles, modals, chart init)
- **Icons:** Lucide via CDN — `<i data-lucide="icon-name">` + `lucide.createIcons()`
- **Charts:** Chart.js via CDN (see Chart.js section below)

Do not introduce React, Vue, Tailwind, shadcn, or Bootstrap unless the user explicitly asks.

---

## Before you design: check what exists

If project files are available, open `base.html`, the main CSS file, and one or two existing templates before generating anything. Reuse:

- **CSS custom properties** (`--color-primary`, `--color-bg`, `--space-*`, etc.)
- **Existing component classes** — `.card`, `.btn`, `.input`, `.badge`, `.table`
- **Base layout** — sidebar? topbar? container width? Follow it.

If files aren't available and the request is non-trivial, ask the user for a screenshot or a pasted template. One screenshot saves three rounds of revision.

---

## Design language

### Color tokens (light mode defaults)

```css
:root {
  /* Backgrounds */
  --color-bg:           #F7F8FA;
  --color-surface:      #FFFFFF;
  --color-surface-2:    #F3F4F6;  /* subtle inset areas */

  /* Borders */
  --color-border:       #E5E7EB;
  --color-border-focus: #6366F1;

  /* Text */
  --color-text:         #111827;
  --color-text-muted:   #6B7280;
  --color-text-subtle:  #9CA3AF;

  /* Primary accent */
  --color-primary:      #6366F1;  /* indigo */
  --color-primary-hover:#4F46E5;
  --color-primary-light:#EEF2FF;

  /* Semantic */
  --color-income:       #10B981;  /* green  - income / positive */
  --color-expense:      #EF4444;  /* red    - expense / negative */
  --color-warning:      #F59E0B;  /* amber  - warnings / budget alerts */
  --color-info:         #3B82F6;  /* blue   - neutral info */

  /* Shadows */
  --shadow-card: 0 1px 2px rgba(0,0,0,0.04), 0 1px 3px rgba(0,0,0,0.06);
  --shadow-modal: 0 8px 24px rgba(0,0,0,0.12);

  /* Radius */
  --radius-sm:   8px;
  --radius-md:   12px;
  --radius-lg:   16px;
  --radius-full: 9999px;

  /* Spacing (8px grid) */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
}
```

### Dark mode tokens

Implement dark mode with a `[data-theme="dark"]` attribute on `<html>`. Toggle it with a small JS snippet and persist via `localStorage`.

```css
[data-theme="dark"] {
  --color-bg:           #0F1117;
  --color-surface:      #1A1D27;
  --color-surface-2:    #222536;

  --color-border:       #2E3347;
  --color-border-focus: #818CF8;

  --color-text:         #F9FAFB;
  --color-text-muted:   #9CA3AF;
  --color-text-subtle:  #6B7280;

  --color-primary:      #818CF8;
  --color-primary-hover:#6366F1;
  --color-primary-light:#1E1F3B;

  --color-income:       #34D399;
  --color-expense:      #F87171;
  --color-warning:      #FCD34D;
  --color-info:         #60A5FA;

  --shadow-card: 0 1px 2px rgba(0,0,0,0.3), 0 1px 3px rgba(0,0,0,0.4);
  --shadow-modal: 0 8px 24px rgba(0,0,0,0.5);
}
```

**Dark mode toggle (JS, add to `base.html`):**
```js
const root = document.documentElement;
const saved = localStorage.getItem('theme') || 'light';
root.setAttribute('data-theme', saved);

function toggleTheme() {
  const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  root.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
}
```

**Toggle button in nav:**
```html
<button onclick="toggleTheme()" class="btn-icon" aria-label="Toggle theme">
  <i data-lucide="sun" class="icon-light-only"></i>
  <i data-lucide="moon" class="icon-dark-only"></i>
</button>
```

```css
[data-theme="light"] .icon-dark-only  { display: none; }
[data-theme="dark"]  .icon-light-only { display: none; }
```

### Typography

```css
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-size: 16px;
  color: var(--color-text);
  background: var(--color-bg);
}
/* Type scale: 12 / 14 / 16 / 20 / 24 / 32 */
/* Weights: 400 body, 500 medium, 600 semibold */
/* Always use tabular nums for amounts: */
.amount { font-variant-numeric: tabular-nums; font-weight: 600; }
```

### Spacing & layout

- **8px grid** — use multiples of 4px or 8px only. No 13px, no 27px.
- Cards: `padding: var(--space-6)`, `border-radius: var(--radius-md)`
- Forms: `gap: var(--space-4)` between fields
- Tables: `padding: var(--space-3) var(--space-4)` per cell

### Shadows & borders

- Cards: `box-shadow: var(--shadow-card)` + `border: 1px solid var(--color-border)`
- Modals: `box-shadow: var(--shadow-modal)`
- No glows, no heavy drop shadows, no gradients unless explicitly asked

---

## Icons: Lucide

Load once in `base.html`:
```html
<script src="https://unpkg.com/lucide@latest"></script>
```
Call after DOM ready (and after dynamic inserts):
```js
lucide.createIcons();
```

Size via CSS: 16px inline with text, 20px in buttons, 24px for section headers.

Spendly icon vocabulary:
- Expense: `arrow-down-right`, `shopping-bag`, `credit-card`
- Income: `arrow-up-right`, `wallet`, `trending-up`
- Budget: `target`, `pie-chart`
- Category: `tag`, `folder`
- Add: `plus`, `plus-circle`
- Settings: `settings`, `sliders-horizontal`
- Date: `calendar`, `clock`
- Search/filter: `search`, `filter`
- Theme toggle: `sun`, `moon`
- Auth: `log-in`, `log-out`, `user`, `lock`
- Reports: `bar-chart-2`, `line-chart`, `file-text`

One icon per button, one per section heading — don't over-sprinkle.

---

## Chart.js integration

Load via CDN in `base.html` (after Lucide):
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

### Recommended chart types for Spendly

| Use case | Chart type | Notes |
|---|---|---|
| Monthly spend trend | `line` | Fill under curve, smooth tension |
| Category breakdown | `doughnut` | Center label showing total |
| Income vs expense | `bar` | Grouped, 2 datasets |
| Daily spending | `bar` | Single dataset, color-coded by amount |
| Budget progress | Custom CSS bar | Don't use Chart.js for simple bars |

### Chart color palette (use CSS vars via JS)

```js
// Read CSS tokens for chart colors — always do this so dark mode works
function getCSSVar(name) {
  return getComputedStyle(document.documentElement)
    .getPropertyValue(name).trim();
}

const chartColors = {
  primary:  getCSSVar('--color-primary'),
  income:   getCSSVar('--color-income'),
  expense:  getCSSVar('--color-expense'),
  muted:    getCSSVar('--color-text-subtle'),
  surface:  getCSSVar('--color-surface'),
  border:   getCSSVar('--color-border'),
};
```

### Shared Chart.js defaults

Apply these globally once per page for consistent styling:

```js
Chart.defaults.font.family = getComputedStyle(document.body).fontFamily;
Chart.defaults.color = getCSSVar('--color-text-muted');
Chart.defaults.borderColor = getCSSVar('--color-border');
Chart.defaults.plugins.legend.position = 'bottom';
Chart.defaults.plugins.tooltip.backgroundColor = getCSSVar('--color-surface');
Chart.defaults.plugins.tooltip.titleColor = getCSSVar('--color-text');
Chart.defaults.plugins.tooltip.bodyColor = getCSSVar('--color-text-muted');
Chart.defaults.plugins.tooltip.borderColor = getCSSVar('--color-border');
Chart.defaults.plugins.tooltip.borderWidth = 1;
```

### Example: Monthly spend line chart

```js
const ctx = document.getElementById('spend-trend-chart').getContext('2d');
new Chart(ctx, {
  type: 'line',
  data: {
    labels: {{ months | tojson }},      // passed from Flask route
    datasets: [{
      label: 'Expenses',
      data: {{ monthly_totals | tojson }},
      borderColor: chartColors.expense,
      backgroundColor: chartColors.expense + '1A', // 10% opacity fill
      tension: 0.4,
      fill: true,
      pointRadius: 4,
      pointHoverRadius: 6,
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: { beginAtZero: true, grid: { color: getCSSVar('--color-border') } },
      x: { grid: { display: false } }
    }
  }
});
```

**Important:** wrap canvas in a sized container, not the canvas itself:
```html
<div class="chart-container" style="position:relative; height:260px;">
  <canvas id="spend-trend-chart"></canvas>
</div>
```

**Dark mode + charts:** Since `getCSSVar()` reads live CSS variables, charts automatically use dark mode colors if you re-initialize after theme toggle, or use `MutationObserver` on `<html>` to detect theme changes and call `chart.update()`.

---

## Page examples

### Auth pages (login / register)

- **Layout:** centered, single-column, max-width 400px, vertically centered on viewport
- **Surface:** white card on `--color-bg`, logo/app name above form
- **Fields:** email + password for login; name + email + password + confirm for register
- **CTA:** full-width primary button, subtle link to switch between login/register
- **No sidebar** — auth pages are standalone, do not extend the main layout

```
{# templates/auth/login.html #}
{% extends "auth_base.html" %}   {# a minimal base without sidebar #}
{% block content %}
<div class="auth-wrapper">
  <div class="auth-card">
    <div class="auth-header">
      <i data-lucide="wallet" class="auth-logo-icon"></i>
      <h1 class="auth-title">Spendly</h1>
      <p class="auth-subtitle">Sign in to your account</p>
    </div>
    <form method="POST" action="{{ url_for('auth.login') }}" class="auth-form">
      {{ form.hidden_tag() }}  {# CSRF if using Flask-WTF #}
      <div class="field-group">
        <label for="email">Email</label>
        <input type="email" id="email" name="email" class="input" required>
      </div>
      <div class="field-group">
        <label for="password">Password</label>
        <input type="password" id="password" name="password" class="input" required>
      </div>
      <button type="submit" class="btn btn-primary btn-full">Sign in</button>
    </form>
    <p class="auth-footer">No account? <a href="{{ url_for('auth.register') }}">Register</a></p>
  </div>
</div>
{% endblock %}
```

---

### Reports page

**UI plan:**
- Date range selector (this month / last 3 months / custom) at the top
- 3 summary pills: total income, total expenses, net savings
- Line chart: monthly spend trend (Chart.js)
- Doughnut chart: spend by category (Chart.js)
- Table: top 10 transactions in the period
- Export to CSV button (Flask route returns a file download)

**Flask route should pass:**
```python
@app.route('/reports')
def reports():
    return render_template('reports.html',
        months=months,           # list of month labels
        monthly_totals=totals,   # list of floats
        category_labels=labels,  # list of strings
        category_totals=amounts, # list of floats
        top_transactions=txns,   # list of dicts
        period_summary=summary,  # dict: income, expense, net
    )
```

---

### Settings page

**UI plan:**
- Sections as stacked cards (not tabs, to keep it simple):
  1. **Profile** — name, email, change password
  2. **Preferences** — currency symbol, date format, default category
  3. **Appearance** — theme toggle (light/dark), already implemented via `toggleTheme()`
  4. **Danger zone** — delete account (red button, confirm modal)
- Each section has a heading, a divider, its fields, and a Save button scoped to that section
- Settings page does **not** need a full form submit — each section can POST independently to keep UX clean

---

## Output structure

When fulfilling a design request, always structure your response like this:

### 1. UI plan (2–5 bullets)
State key sections, UX decisions, and any assumptions you're making. Keep it tight.

### 2. Code
- **Template** — full Jinja2 with `{% extends "base.html" %}` and `{% block content %}`
- **CSS** — scoped with a page/component prefix (`.reports-...`, `.settings-...`)
- **JS** — only if needed; vanilla, no frameworks

Each file in its own fenced code block with a path annotation.

### 3. Integration note (1–3 lines)
Flask route, template variables expected, any new dependency.

---

## What to avoid

- Generic/dated looks — no default browser styles, no sharp corners, no Bootstrap 3 vibes
- Inconsistent spacing — if a card uses `var(--space-6)` padding, all cards do
- Random accent colors — one primary, semantic colors for meaning, everything else neutral
- Hard-coded color values — always use CSS custom properties so dark mode works automatically
- Charts with hard-coded colors — always read from CSS vars via `getCSSVar()`
- Heavy shadows or gradients — restraint reads as quality in finance UIs
- Mobile afterthought — stack cards vertically, make tables scroll horizontally below 768px

---

## Handling ambiguity

Make reasonable assumptions and state them in the UI plan. Don't pepper the user with questions for things you can reasonably decide. Do ask when the answer genuinely changes the output — e.g. *"Is this a modal or a full page?"*