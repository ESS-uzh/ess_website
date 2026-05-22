# pelicanconf.py
from slugify import slugify
import os, sys, json
from pathlib import Path

sys.path.insert(0, os.path.abspath("."))
from generate_maps import generate_map

# Paths
DATA_DIR = Path("content/data")
TOPICS_FILE = DATA_DIR / "topics.json"
PROJECTS_FILE = DATA_DIR / "projects.json"

# Load JSON
with open(TOPICS_FILE, "r", encoding="utf-8") as f:
    ALL_TOPICS = json.load(f)

with open(PROJECTS_FILE, "r", encoding="utf-8") as f:
    ALL_PROJECTS = json.load(f)


def normalize_project(p):
    return {
        "id": p.get("id"),
        "name": p.get("name", "Untitled"),
        "description": p.get("description") or p.get("short_description", ""),
        "img": p.get("img", ""),
        "lat": p.get("lat"),
        "lon": p.get("lon"),
        "location": p.get("location", ""),
        "tags": p.get("tags", []),
        "polygon": p.get("polygon", []),
    }


ALL_PROJECTS = [normalize_project(p) for p in ALL_PROJECTS]

# Select by IDs instead of sorting
RECENT_PROJECT_IDS = [8, 6]  # manual choice
RECENT_PROJECTS = [p for p in ALL_PROJECTS if p["id"] in RECENT_PROJECT_IDS]

JINJA_FILTERS = {
    "slugify": slugify,
}

# Pass to Jinja
JINJA_GLOBALS = {
    "all_topics": ALL_TOPICS,
    "recent_projects": RECENT_PROJECTS,
    "all_projects": ALL_PROJECTS,
    "generate_map": generate_map,
}

# ---- Site info ----
AUTHOR = "Your Name"
SITENAME = "Your Site"
SITEURL = ""

PATH = "content"
TIMEZONE = "Europe/Zurich"
DEFAULT_LANG = "en"

# ---- Theme ----
THEME = "themes/mytheme2"  # adjust if theme is at root
# Do NOT set THEME_STATIC_DIR or THEME_STATIC_PATHS here

TEMPLATE_EXTENSIONS = [".html", ".htm"]

# ---- Feeds ----
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None

# ---- Plugins ----
PLUGIN_PATHS = ["plugins"]
PLUGINS = [
    "yaml_metadata",
    "load_topics",
    "generate_projects",
    "load_projects",
    "load_people",
]

# ---- URL settings ----
RELATIVE_URLS = True
TOPIC_SAVE_AS = "topics/{slug}.html"
TOPIC_URL = "topics/{slug}.html"
PROJECTPAGE_SAVE_AS = "projects/{slug}.html"
PROJECTPAGE_URL = "projects/{slug}.html"

STATIC_PATHS = ["maps", "images", "extra", "data"]

READERS = {'html': None}

# Topic pages
TOPICPAGE_SAVE_AS = "topics/{slug}.html"
TOPICPAGE_URL = "topics/{slug}.html"

DISPLAY_PAGES_ON_MENU = False


# Debug prints
print("Theme path:", THEME, "-> exists?", os.path.exists(THEME))
print("ALL_PROJECTS:", ALL_PROJECTS[:2])
print("RECENT_PROJECTS:", RECENT_PROJECTS)
