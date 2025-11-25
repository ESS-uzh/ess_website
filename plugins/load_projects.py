from pelican import signals, contents, generators
import json, os


def generate_project_pages(generator):
    projects_path = os.path.join(generator.settings["PATH"], "data", "projects.json")

    with open(projects_path, encoding="utf-8") as f:
        projects = json.load(f)

    # Make it available to templates as `projects`
    generator.context["projects"] = projects

    for project in projects:
        metadata = {
            "title": project["name"],
            "slug": project["name"].lower().replace(" ", "-"),
            "template": "project_page",
        }
        generator.context["project"] = project  # a single dict
        content = project.get("description", "")
        page = contents.Page(content=content, metadata=metadata)
        page.project_data = project

        # Only add map if lat/lon exist
        if project.get("lat") and project.get("lon"):
            page.project_map = f"""
            <div id="project-map" style="width:100%; height:300px;"></div>
            <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
            <script>
            document.addEventListener('DOMContentLoaded', function() {{
                const map = L.map('project-map').setView([{project['lat']}, {project['lon']}], 6);
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                    maxZoom: 18,
                    attribution: '&copy; OpenStreetMap contributors'
                }}).addTo(map);

                const marker = L.marker([{project['lat']}, {project['lon']}]).addTo(map);
                marker.bindPopup("<strong>{project['name']}</strong>");

                if ({json.dumps(project.get('polygon'))}) {{
                    L.polygon({json.dumps(project.get('polygon'))}).addTo(map);
                }}
            }});
            </script>
            """
        else:
            page.project_map = None

        # Append the page to the PagesGenerator
        if hasattr(generator, "pages"):
            generator.pages.append(page)


def register():
    signals.page_generator_finalized.connect(generate_project_pages)
