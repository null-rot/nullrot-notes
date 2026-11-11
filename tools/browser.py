"""Shared headless-Chrome launcher for the PDF/screenshot scripts (Windows, macOS, Linux)."""
import os, shutil, pathlib

CANDIDATES = [
    os.environ.get('CHROME_PATH', ''),
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
    os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe'),
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/usr/bin/google-chrome',
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser',
]


def chrome_path():
    """Path to a Chrome-family browser, or None to use Playwright's bundled Chromium."""
    for c in CANDIDATES:
        if c and os.path.isfile(c):
            return c
    for name in ('google-chrome', 'chromium', 'chromium-browser', 'chrome'):
        found = shutil.which(name)
        if found:
            return found
    return None


def launch(p):
    exe = chrome_path()
    return p.chromium.launch(executable_path=exe, args=['--no-sandbox']) if exe else p.chromium.launch()


def file_url(path):
    """file:// URL that works on every OS (Windows drive letters included)."""
    return pathlib.Path(path).resolve().as_uri()
