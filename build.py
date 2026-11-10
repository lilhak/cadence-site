#!/usr/bin/env python3
"""Builds the Cadence site's static pages. Run: python3 build.py

The pages are plain HTML with relative links, so they work under any path or domain.
Edit the text in pages/*.html (page bodies only), then run this and commit the result.
"""
from pathlib import Path

root = Path(__file__).parent
UPDATED = "November 10, 2026"
COMPANY = "KNP Trading LLC"
EMAIL = "support@use-cadence.app"

PAGES = {
    "index": ("", "Cadence: chores and home tasks that come back on time",
              "Cadence is a chore tracker for the home tasks that come around again. Recurring tasks counted from when you last did them, shared with your household."),
    "support": ("support/", "Cadence support",
                "Help with Cadence: recurring tasks, households, reminders, Cadence Plus and your account."),
    "privacy": ("privacy/", "Cadence privacy policy",
                "What Cadence collects, where it is kept, who it is shared with, and how to delete it."),
    "terms": ("terms/", "Cadence terms of service",
              "The terms for using Cadence, including Cadence Plus subscriptions."),
}


def page(name: str) -> str:
    path, title, description = PAGES[name]
    up = "../" if path else ""
    body = (root / "pages" / f"{name}.html").read_text()
    body = body.replace("{{UPDATED}}", UPDATED).replace("{{COMPANY}}", COMPANY).replace("{{EMAIL}}", EMAIL).replace("{{UP}}", up)

    def nav(target: str, label: str) -> str:
        current = ' aria-current="page"' if target == name else ""
        return f'<a href="{up}{PAGES[target][0]}"{current}>{label}</a>'

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="icon" href="{up}icon.png">
<link rel="stylesheet" href="{up}site.css">
</head>
<body>
<header class="site">
  <a class="brand" href="{up or './'}"><img src="{up}icon.png" alt="" width="36" height="36">Cadence</a>
  <nav>{nav('support', 'Support')}{nav('privacy', 'Privacy')}{nav('terms', 'Terms')}</nav>
</header>
<main>
{body.strip()}
</main>
<footer class="site">
  <p>Cadence is made by {COMPANY}, Sacramento, California, United States.<br>
  <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{up}support/">Support</a> · <a href="{up}privacy/">Privacy</a> · <a href="{up}terms/">Terms</a></p>
</footer>
</body>
</html>
"""


for name, (path, _, _) in PAGES.items():
    out = root / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(name))
    print("wrote", out.relative_to(root))
