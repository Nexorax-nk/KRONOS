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
    
    # Generate highly stylized Mermaid graph code
    graph_lines = ["flowchart TD"]
    
    # Styles
    graph_lines.append("    classDef activeNode fill:#1e1b4b,stroke:#6366f1,stroke-width:2px,color:#fff,rx:10px,ry:10px;")
    graph_lines.append("    classDef deprecatedNode fill:#2d1a1a,stroke:#ef4444,stroke-width:1px,color:#94a3b8,rx:10px,ry:10px;")
    graph_lines.append("    classDef fileNode fill:#0f172a,stroke:#334155,stroke-width:1px,color:#38bdf8,rx:5px,ry:5px;")
    
    for m in memories:
        status_val = m.status.value if hasattr(m.status, 'value') else m.status
        status_class = "activeNode" if status_val == "active" else "deprecatedNode"
        label = f"\"{m.id}<br/>{m.decision[:30]}...\""
        
        # Define memory node
        graph_lines.append(f"    {m.id}[{label}]:::{status_class}")
        
        # Govern relation
        for file in m.governs_files:
            file_id = file.replace("/", "_").replace(".", "_").replace("-", "_")
            graph_lines.append(f"    {file_id}[\"📄 {file}\"]:::fileNode")
            graph_lines.append(f"    {m.id} -->|governs| {file_id}")
            
        # Dependencies
        for dep in m.depends_on:
            graph_lines.append(f"    {dep} -.-> {m.id}")
            
        # Blocks
        for block in m.blocks:
            graph_lines.append(f"    {m.id} -->|blocks| {block}")

    # Fallback if no elements
    if len(graph_lines) == 4:
        graph_lines.append("    Empty[\"No active memories in ledger\"]:::fileNode")

    mermaid_graph_code = "\n".join(graph_lines)

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
        mermaid_graph_code=mermaid_graph_code,
        recent_memories=memories[:10]
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

