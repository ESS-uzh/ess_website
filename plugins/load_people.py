import json
from pelican import signals
from pelican.contents import Page

TEAM_FILE = "content/data/team.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_people_page(generator):
    people = load_json(TEAM_FILE)

    metadata = {
        "title": "Our Team",
        "slug": "people",
        "template": "people",
        "save_as": "people/index.html",
        "url": "people",
    }

    page = Page(
        content="",
        metadata=metadata,
        source_path="people.md",
        context=generator.context,
        settings=generator.settings,
    )

    page.people = people
    generator.pages.append(page)


def register():
    signals.page_generator_finalized.connect(generate_people_page)
