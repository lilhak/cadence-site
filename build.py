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
APP_STORE_URL = "https://apps.apple.com/us/app/cadence-chore-tracker-tasks/id6757681008"
# Set this when the Play Store listing goes live, then rebuild. Empty = "coming soon".
PLAY_URL = ""

APPLE_SVG = '<svg class="logo" viewBox="2 0 20 24" aria-hidden="true" focusable="false"><path d="M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"/></svg>'
PLAY_SVG = '<svg class="logo" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M22.018 13.298l-3.919 2.218-3.515-3.493 3.543-3.521 3.891 2.202a1.49 1.49 0 0 1 0 2.594zM1.337.924a1.486 1.486 0 0 0-.112.568v21.017c0 .217.045.419.124.6l11.155-11.087L1.337.924zm12.207 10.065l3.258-3.238L3.45.195a1.466 1.466 0 0 0-.946-.179l11.04 10.973zm0 2.067l-11 10.933c.298.036.612-.016.906-.183l13.324-7.54-3.23-3.21z"/></svg>'


def store_buttons() -> str:
    ios = f'<a class="get-link" href="{APP_STORE_URL}">{APPLE_SVG}<span><small>Download on the</small>App Store</span></a>'
    if PLAY_URL:
        play = f'<a class="get-link" href="{PLAY_URL}">{PLAY_SVG}<span><small>Get it on</small>Google Play</span></a>'
    else:
        play = f'<span class="get-link is-soon" aria-disabled="true">{PLAY_SVG}<span><small>Coming soon to</small>Google Play</span></span>'
    return f'<div class="get">{ios}{play}</div>'

PAGES = {
    "index": ("", "Cadence: home tasks that come back on time",
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
    body = body.replace("{{UPDATED}}", UPDATED).replace("{{COMPANY}}", COMPANY).replace("{{EMAIL}}", EMAIL).replace("{{UP}}", up).replace("{{STORE_BUTTONS}}", store_buttons())

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
<body class="page-{name}">
<header class="site">
  <a class="brand" href="{up or './'}"><img src="{up}icon.png" alt="" width="36" height="36">Cadence</a>
  <nav>{nav('support', 'Support')}{nav('privacy', 'Privacy')}{nav('terms', 'Terms')}</nav>
</header>
<main>
{body.strip()}
</main>
<footer class="site">
  <p><a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{up}support/">Support</a> · <a href="{up}privacy/">Privacy</a> · <a href="{up}terms/">Terms</a></p>
</footer>
</body>
</html>
"""


for name, (path, _, _) in PAGES.items():
    out = root / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(name))
    print("wrote", out.relative_to(root))
