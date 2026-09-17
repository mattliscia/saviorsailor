#!/usr/bin/env python3
"""Generate the Navy Deployment Packing List pages from packing_list_content.py.

Usage:  python3 scripts/build_packing_list.py
Writes deployment-packing-list.html and deployment-packing-list-<chapter>.html
into the repo root. Markup mirrors about.html so the pages match the site.
"""
import html
import json
import os
import sys
from urllib.parse import quote_plus

sys.path.insert(0, os.path.dirname(__file__))
from packing_list_content import AFFILIATE_TAG, CHAPTERS, HUB  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://saviorsailor.com"
HUB_FILE = HUB["slug"] + ".html"
DATE_PUBLISHED = "2024-05-17"
DATE_MODIFIED = "2026-09-17"
OG_IMAGE = SITE + "/images/ebook.png"
DISCLOSURE = "As an Amazon Associate, Savior Sailor earns from qualifying purchases. Product links on this page are affiliate links; the products and prices are Amazon's, not ours."


def e(s):
    return html.escape(s, quote=True)


def chapter_file(ch):
    return f"{HUB['slug']}-{ch['slug']}.html"


def chapter_items(ch):
    if "items" in ch:
        return ch["items"]
    return [i for g in ch["groups"] for i in g["items"]]


def amazon_url(item):
    if item.get("asin"):
        return f"https://www.amazon.com/dp/{item['asin']}?tag={AFFILIATE_TAG}"
    return f"https://www.amazon.com/s?k={quote_plus(item['search'])}&tag={AFFILIATE_TAG}"


def head(title, description, filename, jsonld):
    url = f"{SITE}/{filename}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">

    <title>{e(title)}</title>
    <meta name="description" content="{e(description)}">
    <meta name="author" content="Alex Velichko">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{url}">

    <!-- Open Graph -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{e(title)}">
    <meta property="og:description" content="{e(description)}">
    <meta property="og:image" content="{OG_IMAGE}">
    <meta property="og:url" content="{url}">
    <meta property="og:site_name" content="Savior Sailor">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{e(title)}">
    <meta name="twitter:description" content="{e(description)}">
    <meta name="twitter:image" content="{OG_IMAGE}">

    <link rel="shortcut icon" href="favicon.ico">

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        'navy': {{
                            50: '#E8F0F7',
                            100: '#C5D9EB',
                            500: '#1E3A5F',
                            600: '#1A3352',
                        }},
                        'sunny': {{
                            300: '#FBE89A',
                            400: '#F9E06D',
                            500: '#F7D547',
                            600: '#E5C33A',
                        }},
                        'sky': {{
                            100: '#E8F4FA',
                            200: '#B8DCF0',
                            500: '#6BB8E0',
                            600: '#4A9FCC',
                        }},
                    }},
                    fontFamily: {{
                        'sans': ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
                    }},
                }},
            }},
        }}
    </script>

    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-KT701YNK8L"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-KT701YNK8L');
    </script>

    <script type="application/ld+json">
{json.dumps(jsonld, indent=4, ensure_ascii=False)}
    </script>

    <style>
        html {{ scroll-behavior: smooth; }}
    </style>
</head>
<body class="font-sans text-gray-700 antialiased">
"""


NAV = f"""
    <!-- Navigation -->
    <header class="fixed w-full top-0 z-50 bg-white/95 backdrop-blur-sm shadow-sm">
        <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16 md:h-20">
                <a href="index.html" class="flex-shrink-0">
                    <img src="images/logo.png" alt="Savior Sailor" class="h-12 md:h-14 w-auto">
                </a>
                <div class="hidden md:flex items-center space-x-8">
                    <a href="index.html" class="text-gray-600 hover:text-navy-500 font-medium transition">Home</a>
                    <a href="about.html" class="text-gray-600 hover:text-navy-500 font-medium transition">About</a>
                    <a href="care-packages.html" class="text-gray-600 hover:text-navy-500 font-medium transition">Care Packages</a>
                    <a href="sponsor-a-sailor.html" class="text-gray-600 hover:text-navy-500 font-medium transition">Sponsor</a>
                    <a href="gallery.html" class="text-gray-600 hover:text-navy-500 font-medium transition">Gallery</a>
                    <a href="{HUB_FILE}" class="text-navy-500 font-semibold border-b-2 border-sunny-500">Packing List</a>
                </div>
                <a href="care-packages.html" class="hidden md:inline-flex bg-navy-500 text-white px-5 py-2.5 rounded-full font-semibold hover:bg-navy-600 transition shadow-lg shadow-navy-500/25">
                    Send a Package
                </a>
                <button id="mobile-menu-btn" class="md:hidden p-2 rounded-lg hover:bg-gray-100" aria-label="Open menu">
                    <svg class="w-6 h-6 text-navy-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
                    </svg>
                </button>
            </div>
            <div id="mobile-menu" class="hidden md:hidden pb-4">
                <div class="flex flex-col space-y-3">
                    <a href="index.html" class="text-gray-600 hover:text-navy-500 font-medium py-2">Home</a>
                    <a href="about.html" class="text-gray-600 hover:text-navy-500 font-medium py-2">About</a>
                    <a href="care-packages.html" class="text-gray-600 hover:text-navy-500 font-medium py-2">Care Packages</a>
                    <a href="sponsor-a-sailor.html" class="text-gray-600 hover:text-navy-500 font-medium py-2">Sponsor</a>
                    <a href="gallery.html" class="text-gray-600 hover:text-navy-500 font-medium py-2">Gallery</a>
                    <a href="{HUB_FILE}" class="text-navy-500 font-semibold py-2">Packing List</a>
                    <a href="care-packages.html" class="bg-navy-500 text-white px-5 py-3 rounded-full font-semibold text-center mt-2">Send a Package</a>
                </div>
            </div>
        </nav>
    </header>
"""

CTA = """
        <!-- CTA Section -->
        <section class="py-20 bg-gradient-to-r from-navy-500 to-navy-600">
            <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                <h2 class="text-3xl sm:text-4xl font-bold text-white mb-6">Don't Want to Shop All of This Yourself?</h2>
                <p class="text-xl text-white/80 mb-10 max-w-2xl mx-auto">
                    Our care packages are built from this exact list by sailors who have lived it. Send one to a sailor you love, or to one who has nobody sending anything.
                </p>
                <div class="flex flex-col sm:flex-row gap-4 justify-center">
                    <a href="care-packages.html" class="inline-flex items-center justify-center bg-sunny-500 text-navy-600 px-8 py-4 rounded-full text-lg font-bold hover:bg-sunny-400 transition shadow-lg">
                        Send a Care Package
                    </a>
                    <a href="sponsor-a-sailor.html" class="inline-flex items-center justify-center border-2 border-white text-white px-8 py-4 rounded-full text-lg font-bold hover:bg-white hover:text-navy-500 transition">
                        Sponsor a Sailor
                    </a>
                </div>
            </div>
        </section>
"""

FOOTER = f"""
    <!-- Footer -->
    <footer class="bg-navy-600 text-white py-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid md:grid-cols-4 gap-12">
                <div class="md:col-span-2">
                    <img src="images/logo.png" alt="Savior Sailor" class="h-16 mb-4  ">
                    <p class="text-white/70 mb-6 max-w-md">
                        Supporting sailors at sea with care packages designed by veterans. Founded by FCA2(SW) Alex Velichko with 8+ years of Navy service.
                    </p>
                    <div class="flex gap-4">
                        <a href="https://www.facebook.com/profile.php?id=100075436362467" target="_blank" class="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center hover:bg-sunny-500 transition" aria-label="Facebook">
                            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                        </a>
                        <a href="https://www.instagram.com/savior.sailor/" target="_blank" class="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center hover:bg-sunny-500 transition" aria-label="Instagram">
                            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
                        </a>
                        <a href="https://www.youtube.com/channel/UCyII3UTiO0U8al3tDQ8OHOA" target="_blank" class="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center hover:bg-sunny-500 transition" aria-label="YouTube">
                            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                        </a>
                    </div>
                </div>
                <div>
                    <h4 class="font-semibold text-lg mb-4">Quick Links</h4>
                    <ul class="space-y-3">
                        <li><a href="about.html" class="text-white/70 hover:text-sunny-400 transition">About Us</a></li>
                        <li><a href="care-packages.html" class="text-white/70 hover:text-sunny-400 transition">Care Packages</a></li>
                        <li><a href="sponsor-a-sailor.html" class="text-white/70 hover:text-sunny-400 transition">Become a Sponsor</a></li>
                        <li><a href="sponsors.html" class="text-white/70 hover:text-sunny-400 transition">Our Sponsors</a></li>
                        <li><a href="gallery.html" class="text-white/70 hover:text-sunny-400 transition">Gallery</a></li>
                        <li><a href="{HUB_FILE}" class="text-white/70 hover:text-sunny-400 transition">Packing List</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="font-semibold text-lg mb-4">Contact</h4>
                    <ul class="space-y-3">
                        <li><a href="mailto:saviorsailor75@gmail.com" class="text-white/70 hover:text-sunny-400 transition">saviorsailor75@gmail.com</a></li>
                        <li><a href="https://docs.google.com/forms/d/e/1FAIpQLSdy7ZWlisX8ndzR_FoNdvDSQmBSmhYnlDePDNXNyb4_Y5ce7Q/viewform?usp=sf_link" target="_blank" class="text-white/70 hover:text-sunny-400 transition">Request a Package</a></li>
                        <li><a href="terms.html" class="text-white/70 hover:text-sunny-400 transition">Terms & Conditions</a></li>
                    </ul>
                </div>
            </div>
            <div class="border-t border-white/20 mt-12 pt-8 text-center">
                <p class="text-white/60">&copy; 2026 Savior Sailor. All Rights Reserved.</p>
            </div>
        </div>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>
"""

ARROW_RIGHT = '<svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>'
ARROW_LEFT = '<svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>'
EXTERNAL = '<svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>'


def author_block():
    return """
                <div class="flex items-center gap-4">
                    <img src="images/alex.png" alt="FCA2(SW) Alex Velichko" class="w-14 h-14 rounded-full object-cover shadow-md">
                    <div>
                        <p class="font-bold text-navy-500">FCA2(SW) Alex Velichko</p>
                        <p class="text-sm text-gray-500">Founder, Savior Sailor &middot; 8+ years U.S. Navy, 22+ months at sea</p>
                    </div>
                </div>"""


def jsonld_article(title, description, filename):
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "image": OG_IMAGE,
        "author": {"@type": "Person", "name": "Alex Velichko", "url": f"{SITE}/about.html"},
        "publisher": {
            "@type": "Organization",
            "name": "Savior Sailor",
            "logo": {"@type": "ImageObject", "url": f"{SITE}/images/logo.png"},
        },
        "datePublished": DATE_PUBLISHED,
        "dateModified": DATE_MODIFIED,
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{SITE}/{filename}"},
        "isPartOf": {"@type": "WebPage", "@id": f"{SITE}/{HUB_FILE}", "name": HUB["title"]},
    }


def item_html(item, n, heading_tag):
    alex = f'\n                        <p class="text-gray-600 leading-relaxed mb-2">{e(item["alex"])}</p>' if item["alex"] else ""
    return f"""
                <article id="{e(slugify(item['name']))}" class="flex gap-4 sm:gap-6 py-8 border-b border-gray-100 last:border-0">
                    <div class="flex-shrink-0 w-10 h-10 rounded-full bg-navy-100 text-navy-600 font-bold flex items-center justify-center">{n}</div>
                    <div class="min-w-0">
                        <{heading_tag} class="text-xl font-bold text-navy-500 mb-2">{e(item['name'])}</{heading_tag}>{alex}
                        <p class="text-gray-600 leading-relaxed">{e(item['why'])}</p>
                        <a href="{amazon_url(item)}" target="_blank" rel="sponsored nofollow noopener" class="inline-flex items-center mt-3 text-sm font-semibold text-navy-500 hover:text-sunny-600 transition">
                            View on Amazon{EXTERNAL}
                        </a>
                    </div>
                </article>"""


def slugify(name):
    out = "".join(c.lower() if c.isalnum() else "-" for c in name)
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-")


def chapter_page(idx, ch):
    n_total = len(CHAPTERS)
    prev_ch = CHAPTERS[idx - 1] if idx > 0 else None
    next_ch = CHAPTERS[idx + 1] if idx + 1 < n_total else None
    filename = chapter_file(ch)
    items = chapter_items(ch)

    if "items" in ch:
        body_items = "".join(item_html(it, i + 1, "h2") for i, it in enumerate(items))
    else:
        parts, counter = [], 0
        for g in ch["groups"]:
            parts.append(f'\n                <h2 class="text-2xl sm:text-3xl font-bold text-navy-500 pt-10 pb-2 border-b-2 border-sunny-500">{e(g["heading"])}</h2>')
            for it in g["items"]:
                counter += 1
                parts.append(item_html(it, counter, "h3"))
        body_items = "".join(parts)

    prev_link = (
        f"""<a href="{chapter_file(prev_ch)}" class="flex-1 group bg-sky-100 rounded-2xl p-6 hover:bg-sky-200 transition">
                        <span class="inline-flex items-center text-sm font-semibold text-gray-500 mb-1">{ARROW_LEFT}Previous chapter</span>
                        <span class="block text-lg font-bold text-navy-500">{e(prev_ch['label'])}</span>
                    </a>"""
        if prev_ch
        else f"""<a href="{HUB_FILE}" class="flex-1 group bg-sky-100 rounded-2xl p-6 hover:bg-sky-200 transition">
                        <span class="inline-flex items-center text-sm font-semibold text-gray-500 mb-1">{ARROW_LEFT}Back to</span>
                        <span class="block text-lg font-bold text-navy-500">The full packing list</span>
                    </a>"""
    )
    next_link = (
        f"""<a href="{chapter_file(next_ch)}" class="flex-1 group bg-navy-500 rounded-2xl p-6 hover:bg-navy-600 transition text-right">
                        <span class="inline-flex items-center justify-end text-sm font-semibold text-white/70 mb-1">Next chapter{ARROW_RIGHT}</span>
                        <span class="block text-lg font-bold text-white">{e(next_ch['label'])}</span>
                    </a>"""
        if next_ch
        else f"""<a href="{HUB_FILE}" class="flex-1 group bg-navy-500 rounded-2xl p-6 hover:bg-navy-600 transition text-right">
                        <span class="inline-flex items-center justify-end text-sm font-semibold text-white/70 mb-1">You made it{ARROW_RIGHT}</span>
                        <span class="block text-lg font-bold text-white">Back to the full packing list</span>
                    </a>"""
    )

    chapter_links = "".join(
        f'\n                        <li><a href="{chapter_file(c)}" class="{"text-navy-500 font-bold" if c is ch else "text-gray-600 hover:text-navy-500"} transition">{i + 1}. {e(c["label"])}</a></li>'
        for i, c in enumerate(CHAPTERS)
    )

    page = head(ch["meta_title"], ch["description"], filename, jsonld_article(ch["title"], ch["description"], filename))
    page += NAV
    page += f"""
    <main>
        <!-- Hero Section -->
        <section class="pt-32 pb-12 bg-gradient-to-b from-sky-100 to-white">
            <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
                <nav aria-label="Breadcrumb" class="text-sm text-gray-500 mb-6">
                    <a href="index.html" class="hover:text-navy-500 transition">Home</a>
                    <span class="mx-2">/</span>
                    <a href="{HUB_FILE}" class="hover:text-navy-500 transition">Deployment Packing List</a>
                    <span class="mx-2">/</span>
                    <span class="text-navy-500 font-medium">{e(ch['label'])}</span>
                </nav>
                <span class="inline-block bg-navy-100 text-navy-600 px-4 py-1 rounded-full text-sm font-semibold mb-4">Chapter {idx + 1} of {n_total} &middot; {len(items)} items</span>
                <h1 class="text-4xl sm:text-5xl font-extrabold text-navy-500 mb-6">{e(ch['title'])}</h1>
                <p class="text-xl text-gray-600 leading-relaxed mb-8">{e(ch['intro'])}</p>{author_block()}
            </div>
        </section>

        <!-- Items -->
        <section class="py-8 bg-white">
            <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
                <p class="text-sm text-gray-500 bg-gray-50 rounded-xl px-4 py-3 mb-4">{e(DISCLOSURE)}</p>{body_items}
            </div>
        </section>

        <!-- Chapter navigation -->
        <section class="py-12 bg-white">
            <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex flex-col sm:flex-row gap-4 mb-10">
                    {prev_link}
                    {next_link}
                </div>
                <div class="bg-gray-50 rounded-2xl p-6">
                    <h2 class="text-lg font-bold text-navy-500 mb-4">All chapters</h2>
                    <ul class="grid sm:grid-cols-2 gap-x-8 gap-y-2">{chapter_links}
                    </ul>
                    <p class="mt-6 text-gray-600">Prefer the original? <a href="SAVIOR_SAILOR_EBOOK.pdf" target="_blank" class="font-semibold text-navy-500 hover:text-sunny-600 transition">Download the full ebook (PDF)</a>.</p>
                </div>
            </div>
        </section>
{CTA}
    </main>
"""
    page += FOOTER
    return filename, page


def hub_page():
    filename = HUB_FILE
    total_items = sum(len(chapter_items(c)) for c in CHAPTERS)
    cards = ""
    for i, c in enumerate(CHAPTERS):
        cards += f"""
                    <a href="{chapter_file(c)}" class="group bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 p-8 flex flex-col">
                        <span class="text-sm font-semibold text-sunny-600 mb-2">Chapter {i + 1} &middot; {len(chapter_items(c))} items</span>
                        <h3 class="text-xl font-bold text-navy-500 mb-3 group-hover:text-navy-600">{e(c['label'])}</h3>
                        <p class="text-gray-600 mb-6 flex-1">{e(c['description'].split(' Chapter ')[0])}</p>
                        <span class="inline-flex items-center text-navy-500 font-semibold group-hover:text-sunny-600 transition">Read chapter{ARROW_RIGHT}</span>
                    </a>"""

    intro_ps = "".join(f'\n                            <p>{e(p)}</p>' for p in HUB["intro"])
    first = chapter_file(CHAPTERS[0])

    jsonld = jsonld_article(HUB["title"], HUB["description"], filename)
    jsonld.pop("isPartOf")
    jsonld["hasPart"] = [
        {"@type": "Article", "headline": c["title"], "url": f"{SITE}/{chapter_file(c)}"} for c in CHAPTERS
    ]

    page = head(HUB["meta_title"], HUB["description"], filename, jsonld)
    page += NAV
    page += f"""
    <main>
        <!-- Hero Section -->
        <section class="pt-32 pb-16 bg-gradient-to-b from-sky-100 to-white">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="grid lg:grid-cols-5 gap-12 items-center">
                    <div class="lg:col-span-3">
                        <span class="inline-block bg-navy-100 text-navy-600 px-4 py-1 rounded-full text-sm font-semibold mb-4">Free Guide &middot; {total_items} items</span>
                        <h1 class="text-4xl sm:text-5xl font-extrabold text-navy-500 mb-6">{e(HUB['title'])}</h1>
                        <p class="text-xl text-gray-600 leading-relaxed mb-8">Everything to pack for a Navy deployment, from a sailor who spent 22 months at sea and asked 30 more what they wished they had brought. Organized by category, with a reason for every item.</p>
                        <div class="flex flex-col sm:flex-row gap-4 mb-8">
                            <a href="{first}" class="inline-flex items-center justify-center bg-navy-500 text-white px-8 py-4 rounded-full text-lg font-bold hover:bg-navy-600 transition shadow-lg shadow-navy-500/25">
                                Start with Chapter 1{ARROW_RIGHT}
                            </a>
                            <a href="SAVIOR_SAILOR_EBOOK.pdf" target="_blank" class="inline-flex items-center justify-center border-2 border-navy-500 text-navy-500 px-8 py-4 rounded-full text-lg font-bold hover:bg-navy-500 hover:text-white transition">
                                Download the full ebook (PDF)
                            </a>
                        </div>{author_block()}
                    </div>
                    <div class="lg:col-span-2 relative max-w-sm mx-auto w-full">
                        <div class="absolute -inset-4 bg-sunny-400 rounded-3xl transform rotate-3"></div>
                        <img src="images/ebook.png" alt="Cover of the Savior Sailor ebook: 20+ Essentials for Deployment" class="relative rounded-3xl shadow-2xl w-full">
                    </div>
                </div>
            </div>
        </section>

        <!-- Chapters -->
        <section id="chapters" class="py-16 bg-gray-50">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="text-center mb-12">
                    <span class="inline-block bg-sunny-100 text-sunny-600 px-4 py-1 rounded-full text-sm font-semibold mb-4">Read Online</span>
                    <h2 class="text-3xl sm:text-4xl font-bold text-navy-500">The Packing List, Chapter by Chapter</h2>
                </div>
                <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8">{cards}
                </div>
            </div>
        </section>

        <!-- From Alex -->
        <section class="py-16 bg-white">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="grid lg:grid-cols-2 gap-12 items-center">
                    <div class="relative order-2 lg:order-1 max-w-md mx-auto w-full">
                        <div class="absolute -inset-4 bg-sunny-400 rounded-3xl transform -rotate-3"></div>
                        <img src="images/alex.png" alt="FCA2(SW) Alex Velichko - Founder of Savior Sailor" class="relative rounded-3xl shadow-2xl w-full">
                    </div>
                    <div class="order-1 lg:order-2">
                        <h2 class="text-3xl sm:text-4xl font-bold text-navy-500 mb-6">Why I Wrote This List</h2>
                        <div class="space-y-4 text-lg text-gray-600 leading-relaxed">{intro_ps}
                        </div>
                        <div class="flex items-center gap-4 mt-8">
                            <div class="h-16 w-1 bg-sunny-500 rounded-full"></div>
                            <div>
                                <p class="font-bold text-xl text-navy-500">FCA2(SW) Alex Velichko</p>
                                <p class="text-gray-500">Founder, Savior Sailor</p>
                                <p class="text-gray-500">8+ Years U.S. Navy Service</p>
                            </div>
                        </div>
                        <p class="text-sm text-gray-500 mt-8">{e(DISCLOSURE)}</p>
                    </div>
                </div>
            </div>
        </section>
{CTA}
    </main>
"""
    page += FOOTER
    return filename, page


def main():
    written = []
    for idx, ch in enumerate(CHAPTERS):
        fn, content = chapter_page(idx, ch)
        with open(os.path.join(ROOT, fn), "w", encoding="utf-8") as f:
            f.write(content)
        written.append(fn)
    fn, content = hub_page()
    with open(os.path.join(ROOT, fn), "w", encoding="utf-8") as f:
        f.write(content)
    written.append(fn)
    for fn in written:
        print("wrote", fn)


if __name__ == "__main__":
    main()
