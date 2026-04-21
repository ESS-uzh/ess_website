import json
import folium
from pathlib import Path

# Load project data
with open("content/data/projects.json") as f:
    projects = json.load(f)

# Output folder for pre-generated maps
maps_dir = Path("content/maps")
maps_dir.mkdir(exist_ok=True)


def compute_centroid(polygon):
    lats, lons = zip(*polygon)
    return sum(lats) / len(lats), sum(lons) / len(lons)


def generate_map(project):
    zoom_start = 5
    polygon = None

    try:
        data = json.load(open(f"content/polygons/{project['polygon']}"))
        polygon = data["features"][0]["geometry"]["coordinates"][0]
    except:
        pass

    if polygon:
        center = compute_centroid(polygon)
    else:
        center = [10.245731, -28.782217]
        zoom_start = 2

    m = folium.Map(
        location=center,
        zoom_start=zoom_start,
        tiles="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        attr="&copy; OpenStreetMap contributors & CARTO",
    )

    if polygon:
        folium.Polygon(
            locations=polygon, color="blue", fill=True, fill_opacity=0.4
        ).add_to(m)
    if project["lat"] is not None or project["lon"] is not None:
        folium.Marker([project["lat"], project["lon"]], popup=project["name"]).add_to(m)

    return m._repr_html_()


# Generate HTML files for each project map
for project in projects:
    map_html = generate_map(project)
    map_file = maps_dir / f"project_{project['id']}_map.html"
    map_file.write_text(map_html)
