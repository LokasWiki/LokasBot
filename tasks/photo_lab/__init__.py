"""
Photo Lab Archiving Task.

This task automates the archiving of completed photo workshop requests
on Arabic Wikipedia.

The workflow:
1. Reads the main requests page (ويكيبيديا:ورشة الصور/طلبات)
2. Extracts all "طلب ورشة صور" templates
3. Checks each request page for the "منظور" template
4. Archives completed requests to the appropriate archive page
5. Removes archived requests from the main page

Usage:
    python -m tasks.photo_lab.main
"""

__version__ = "1.0.0"
__author__ = "LokasBot"
