import os
from jinja2 import Environment, FileSystemLoader
from typing import List
from .models import Memory

def generate_dashboard(memories: List[Memory], output_path: str):
    """Generates the static HTML dashboard from memories."""
    
    # Calculate stats
    total_memories = len(memories)
    security_count = sum(1 for m in memories if m.security_relevant)
    
    # Mock carbon math for demonstration
    total_kwh = sum(300 for _ in memories) # Dummy logic
    total_co2 = int(total_kwh * 0.4)
    total_trees = int(total_co2 / 21)
    
    # Build dependency links for Mermaid
    dependency_links = []
    for m in memories:
        for dep in m.depends_on:
            dependency_links.append({"source": dep, "target": m.id})
        for block in m.blocks:
            dependency_links.append({"source": m.id, "target": block})

    # Set up Jinja2
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("dashboard.html")

    # Render
    html = template.render(
        total_memories=total_memories,
        security_count=security_count,
        total_carbon=f"~{total_kwh} kWh",
        total_kwh=total_kwh,
        total_co2=total_co2,
        total_trees=total_trees,
        dependency_links=dependency_links,
        recent_memories=memories[:10]
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
