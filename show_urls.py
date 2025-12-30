import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import get_resolver

def show_urls(urllist, depth=0):
    for entry in urllist:
        if hasattr(entry, 'url_patterns'):
            # It's a URLResolver (includes)
            print("  " * depth + f"[Included] {entry.pattern}")
            show_urls(entry.url_patterns, depth + 1)
        else:
            # It's a URLPattern
            print("  " * depth + f"→ {entry.pattern} [{entry.name}]")

resolver = get_resolver()
print("="*60)
print("ALL URL PATTERNS")
print("="*60)
show_urls(resolver.url_patterns)
