# load_topics.py

import json
from pelican import signals
from pelican.contents import Page
from slugify import slugify

TOPICS_FILE = "content/data/topics.json"
PROJECTS_FILE = "content/data/projects.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_topic_pages(generator):
    """Create Pelican Pages for each Topic from topics.json."""

    # Load data
    topics = load_json(TOPICS_FILE)
    projects = load_json(PROJECTS_FILE)

    for topic in topics:
        topic_name = topic["name"]
        topic_slug = slugify(topic_name)

        # Filter projects for this topic
        topic_projects = [p for p in projects if topic_name in p.get("tags", [])]

        # Build map data (skip global locations)
        project_map_data = []  # always define it
        for p in topic_projects:
            if p.get("location") and p.get("location").lower() != "global":
                project_map_data.append(
                    {
                        "name": p["name"],
                        "lat": p.get("lat"),
                        "lon": p.get("lon"),
                        "id": p.get("id"),
                        "polygon": p.get("polygon", None),
                    }
                )

        # Generate HTML for topic map using Leaflet
        topic_map_html = f"""
        <div id="topic-map-{topic_slug}" style="width:100%; height:400px;"></div>
        <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
        <script>
            const map = L.map('topic-map-{topic_slug}').setView([20,0], 2);
            L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                maxZoom: 19
            }}).addTo(map);

            const projects = {json.dumps(project_map_data)};
            projects.forEach(p => {{
                if (p.lat && p.lon) {{
                    L.marker([p.lat, p.lon]).addTo(map)
                     .bindPopup(p.name);
                }}
                if (p.polygon && Array.isArray(p.polygon)) {{
                    L.polygon(p.polygon).addTo(map);
                }}
            }});
        </script>
        """

        # Metadata so Pelican renders it using topic_page.html
        metadata = {
            "title": topic_name,
            "slug": topic_slug,
            "template": "topic_page",
            "save_as": f"topics/{topic_slug}/index.html",
            "url": f"topics/{topic_slug}",
        }

        # Create a Pelican Page
        page = Page(
            content="",  # No markdown body
            metadata=metadata,
            source_path=f"topics/{topic_slug}.md",
            context=generator.context,
            settings=generator.settings,
        )

        # Attach fields used in the template
        page.topic_name = topic_name
        page.topic_description = topic.get("description", "")
        page.projects = topic_projects
        page.topic_map = topic_map_html

        generator.pages.append(page)


# def generate_map_for_single_project(project):
#    """Fallback map function for generate_project.py."""
#    polygon_js = ""
#    if project.get("polygon"):
#        polygon_js = f"L.polygon({project['polygon']}).addTo(map);"
#
#    return f"""
#    <div id="project-map-{project['id']}" style="width:100%; height:300px;"></div>
#    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
#    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
#    <script>
#        const map = L.map('project-map-{project['id']}').setView([{project.get('lat',0)}, {project.get('lon',0)}], 5);
#        L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
#            maxZoom: 19
#        }}).addTo(map);
#        L.marker([{project.get('lat',0)}, {project.get('lon',0)}]).addTo(map)
#         .bindPopup("{project.get('name')}");
#        {polygon_js}
#    </script>
#    """


def generate_map_for_single_project(project):
    """Generate a Leaflet map for a single project, centering and zooming on polygon if available."""

    # Prepare JS for polygon if it exists
    polygon_js = ""
    if project.get("polygon"):
        polygon_js = f"""
        const polygon = L.polygon({json.dumps(project['polygon'])}).addTo(map)
            .bindPopup("{project.get('name', '')}");
        map.fitBounds(polygon.getBounds());  // automatically fit map to polygon
        """

    # If no polygon, show a single marker
    marker_js = ""
    if not project.get("polygon") and project.get("lat") and project.get("lon"):
        marker_js = f"""
        L.marker([{project['lat']}, {project['lon']}]).addTo(map)
            .bindPopup("{project.get('name', '')}");
        map.setView([{project['lat']}, {project['lon']}], 5);  // default zoom
        """

    # If both polygon and lat/lon are missing, fallback to [0,0]
    fallback_js = ""
    if not project.get("polygon") and (
        not project.get("lat") or not project.get("lon")
    ):
        fallback_js = "map.setView([0,0], 2);"

    return f"""
    <div id="project-map-{project['id']}" style="width:100%; height:300px;"></div>
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    <script>
        const map = L.map('project-map-{project['id']}');
        L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            maxZoom: 19
        }}).addTo(map);

        {polygon_js or marker_js or fallback_js}
    </script>
    """


def register():
    signals.page_generator_finalized.connect(generate_topic_pages)
