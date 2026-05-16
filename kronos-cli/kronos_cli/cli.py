import click
import json
import os
from pathlib import Path
from rich.console import Console
from rich.table import Table
from .models import Memory
from .dashboard import generate_dashboard
from .agents.kronos_ask import KronosAskAgent
from .agents.reviewer import MRReviewAgent
from .agents.decision_extractor import DecisionExtractorAgent
from .agents.reply_handler import ReplyHandlerAgent
from .github_client import GitHubClient

console = Console()


@click.group()
def main():
    """KRONOS: Institutional Memory for your codebase."""
    pass

@main.command()
@click.option("--path", default=".kronos", help="Path to the kronos memory directory.")
def validate(path):
    """Validate all memory files in the directory."""
    p = Path(path)
    if not p.exists():
        console.print(f"[red]Error:[/red] Directory {path} does not exist.")
        return

    files = list(p.glob("*.json"))
    if not files:
        console.print(f"[yellow]Warning:[/yellow] No memory files found in {path}.")
        return

    table = Table(title="KRONOS Memory Validation")
    table.add_column("File", style="cyan")
    table.add_column("ID", style="green")
    table.add_column("Status", style="magenta")
    table.add_column("Validation", style="bold")

    valid_count = 0
    for file in files:
        try:
            with open(file, "r") as f:
                data = json.load(f)
                memory = Memory(**data)
                table.add_row(file.name, memory.id, memory.status, "[green]PASSED[/green]")
                valid_count += 1
        except Exception as e:
            table.add_row(file.name, "N/A", "N/A", f"[red]FAILED: {str(e)}[/red]")

    console.print(table)
    console.print(f"\n[bold]Summary:[/bold] {valid_count}/{len(files)} files passed validation.")

@main.command()
@click.option("--path", default=".kronos", help="Path to the kronos memory directory.")
@click.option("--output", default="dashboard.html", help="Output path for the HTML dashboard.")
def dashboard(path, output):
    """Generate the premium visual dashboard."""
    p = Path(path)
    if not p.exists():
        console.print(f"[red]Error:[/red] Directory {path} does not exist.")
        return

    files = list(p.glob("*.json"))
    memories = []
    for file in files:
        try:
            with open(file, "r") as f:
                data = json.load(f)
                memories.append(Memory(**data))
        except Exception:
            continue

    if not memories:
        console.print("[yellow]Warning:[/yellow] No valid memories found to generate dashboard.")
        return

    console.print(f"[cyan]Generating dashboard with {len(memories)} memories...[/cyan]")
    generate_dashboard(memories, output)
    console.print(f"[green]Success![/green] Dashboard generated at: [bold]{output}[/bold]")

@main.command()
@click.argument("question", nargs=-1)
@click.option("--path", default=".kronos", help="Path to the kronos memory directory.")
def ask(question, path):
    """Conversational search: Ask KRONOS about the project's architecture."""
    query = " ".join(question)
    if not query:
        console.print("[red]Error:[/red] Please provide a question. Example: kronos ask Why did we choose Redis?")
        return

    p = Path(path)
    if not p.exists():
        console.print(f"[red]Error:[/red] Directory {path} does not exist.")
        return

    memories = []
    for file in p.glob("*.json"):
        try:
            with open(file, "r") as f:
                memories.append(Memory(**json.load(f)))
        except Exception:
            continue

    if not memories:
        console.print("[yellow]Warning:[/yellow] Memory ledger is empty.")
        return

    if not os.environ.get("ANTHROPIC_API_KEY"):
        console.print("[red]Error:[/red] ANTHROPIC_API_KEY environment variable is required.")
        return

    console.print(f"[cyan]🧠 KRONOS is searching its memory for:[/cyan] {query}\n")
    agent = KronosAskAgent()
    answer = agent.answer_question(query, memories)
    
    console.print(answer)

@main.command("review-pr")
@click.option("--repo", required=True, help="GitHub repository name (e.g., owner/repo)")
@click.option("--pr", required=True, type=int, help="Pull Request number")
@click.option("--path", default=".kronos", help="Path to the kronos memory directory.")
@click.option("--fail-on-conflict", is_flag=True, help="Exit with 1 if a critical conflict is detected.")
def review_pr(repo, pr, path, fail_on_conflict):
    """Run the 5-layer MR Review Agent on a live Pull Request."""
    p = Path(path)
    memories = []
    if p.exists():
        for file in p.glob("*.json"):
            try:
                with open(file, "r") as f:
                    memories.append(Memory(**json.load(f)))
            except Exception:
                continue

    if not os.environ.get("GITHUB_TOKEN"):
        console.print("[red]Error:[/red] GITHUB_TOKEN is required to post comments.")
        return

    gh_client = GitHubClient()
    diff = gh_client.get_pr_diff(repo, pr)
    
    if "Error fetching diff" in diff:
        console.print(f"[red]{diff}[/red]")
        return
        
    console.print(f"[cyan]🧠 KRONOS is running 5-Layer Analysis on PR #{pr}...[/cyan]")
    
    # In a real tool, you would fetch PR title/author via PyGithub
    pr_metadata = {"title": "PR Title", "author": "dev"}
    
    agent = MRReviewAgent()
    comment = agent.analyze(diff, memories, pr_metadata)
    
    gh_client.post_comment(repo, pr, comment)
    console.print("[green]✅ Comment posted successfully![/green]")

    # Check for critical conflict to enforce guardrails
    if fail_on_conflict and ("🔴" in comment or "CRITICAL CONFLICT DETECTED" in comment):
        console.print("[bold red]🚨 GUARDRAIL FAILURE: Critical conflict detected between proposed code and Institutional Memory ledgers![/bold red]")
        import sys
        sys.exit(1)

@main.command("extract-pr")
@click.option("--repo", required=True, help="GitHub repository name")
@click.option("--pr", required=True, type=int, help="Pull Request number")
@click.option("--path", default=".kronos", help="Path to save the memory.")
def extract_pr(repo, pr, path):
    """Post-merge hook to extract architectural decisions from a PR."""
    if not os.environ.get("GITHUB_TOKEN"):
        console.print("[red]Error:[/red] GITHUB_TOKEN is required.")
        return

    gh_client = GitHubClient()
    diff = gh_client.get_pr_diff(repo, pr)
    
    if "Error fetching diff" in diff:
        console.print(f"[red]{diff}[/red]")
        return
        
    console.print(f"[cyan]🧠 KRONOS is extracting decisions from merged PR #{pr}...[/cyan]")
    
    pr_metadata = {"number": str(pr), "author": "merged_dev", "title": "Merge PR changes"}
    extractor = DecisionExtractorAgent()
    memory = extractor.extract(diff, pr_metadata)
    
    # Save the memory to .kronos/
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    memory_file = p / f"memory-00{pr}.json"
    
    # Convert memory back to dict/json safely
    with open(memory_file, "w") as f:
        json.dump(json.loads(memory.json()), f, indent=4)
        
    console.print(f"[green]✅ Successfully extracted memory and saved to {memory_file}![/green]")

@main.command("handle-reply")
@click.option("--repo", required=True, help="GitHub repository name")
@click.option("--pr", required=True, type=int, help="PR/Issue number")
@click.option("--comment", required=True, help="The comment text")
@click.option("--path", default=".kronos", help="Path to the kronos memory directory.")
def handle_reply(repo, pr, comment, path):
    """Processes KRONOS reply commands in PR comments."""
    if not os.environ.get("GITHUB_TOKEN"):
        console.print("[red]Error:[/red] GITHUB_TOKEN is required.")
        return

    p = Path(path)
    memories = []
    if p.exists():
        for file in p.glob("*.json"):
            try:
                with open(file, "r") as f:
                    memories.append(Memory(**json.load(f)))
            except Exception:
                continue

    console.print(f"[cyan]🧠 KRONOS is parsing comment command...[/cyan]")
    handler = ReplyHandlerAgent()
    msg, updated_memories = handler.handle(comment, memories)
    
    if "Memory Evolved!" in msg:
        # Save updated memories back to disk
        for m in updated_memories:
            # Re-write the file
            # Find the file corresponding to the memory ID or create one
            # For simplicity, we search for files with that memory ID inside
            for file in p.glob("*.json"):
                try:
                    with open(file, "r") as f:
                        data = json.load(f)
                    if data.get("id") == m.id:
                        with open(file, "w") as f:
                            json.dump(json.loads(m.json()), f, indent=4)
                except Exception:
                    continue

    gh_client = GitHubClient()
    gh_client.post_comment(repo, pr, msg)
    console.print("[green]✅ Reply handled and response posted![/green]")

if __name__ == "__main__":
    main()


