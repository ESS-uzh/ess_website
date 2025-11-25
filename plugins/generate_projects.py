import json
from pelican import signals, contents
from generate_maps import generate_map  # import your map function
from load_topics import generate_map_for_single_project


class ProjectPage(contents.Page):
    """Custom page for each project."""

    pass


def generate_projects(generator):
    content_path = generator.settings.get("PROJECTS_JSON", "content/data/projects.json")

    with open(content_path, "r", encoding="utf-8") as f:
        projects = json.load(f)

    for project in projects:
        metadata = {
            "title": project.get("name", "Untitled"),
            "template": "project_page",  # uses project_page.html
            "slug": str(project.get("id", project.get("name", ""))).lower(),
        }

        page = ProjectPage(
            content="",
            metadata=metadata,
            settings=generator.settings,
            source_path="projects.json",
            context=generator.context,
        )

        # Attach project data
        page.project = project

        # Generate and attach map if data exists
        try:
            page.project_map = generate_map_for_single_project(project)
        except Exception as e:
            print(f"⚠️  Could not generate map for project {project.get('id')}: {e}")
            page.project_map = None

        generator.pages.append(page)


def register():
    signals.page_generator_finalized.connect(generate_projects)
