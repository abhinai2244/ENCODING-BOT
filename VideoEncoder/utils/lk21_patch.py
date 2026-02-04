import urllib.parse
import re

# Patch re.sre_parse for lk21/exrex compatibility on Python 3.12+
if not hasattr(re, "sre_parse"):
    import re._parser
    re.sre_parse = re._parser

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

# Apply pyrogram save_file patch
from . import pyrogram_patch
