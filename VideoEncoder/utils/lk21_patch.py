import urllib.parse

def safe_urlparse(url):
    try:
        return urllib.parse._urlparse(url)
    except Exception:
        return urllib.parse._urlparse("http://invalid")

# Save original function
urllib.parse._urlparse = urllib.parse.urlparse
urllib.parse.urlparse = safe_urlparse

# Now import lk21 AFTER monkey patch
import lk21
