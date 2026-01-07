import click
import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("tasks.json")

def load_tasks():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

@click.group()
def cli():
    """📌 A simple advanced TODO app (CLI version)."""
    pass

@cli.command()
@click.argument("task")
@click.option("--category", "-c", default="General", help="Category of the task")
@click.option("--due", "-d", help="Due date (YYYY-MM-DD)")
def add(task, category, due):
    """Add a new task."""
    tasks = load_tasks()
    tasks.append({
        "task": task,
        "category": category,
        "due": due,
        "done": False
    })
    save_tasks(tasks)
    click.echo(f" Task added: {task} [Category: {category}, Due: {due}]")

@cli.command()
def list():
    """List all tasks."""
    tasks = load_tasks()
    if not tasks:
        click.echo("📭 No tasks found.")
        return

    for i, t in enumerate(tasks, 1):
        status = "✔" if t["done"] else "❌"
        click.echo(f"{i}. {t['task']} | {t['category']} | Due: {t['due']} | {status}")

@cli.command()
@click.argument("task_id", type=int)
def done(task_id):
    """Mark a task as done."""
    tasks = load_tasks()
    if 0 < task_id <= len(tasks):
        tasks[task_id - 1]["done"] = True
        save_tasks(tasks)
        click.echo(f"🎉 Task {task_id} marked as done!")
    else:
        click.echo("⚠ Invalid task ID.")

@cli.command()
@click.argument("task_id", type=int)
def remove(task_id):
    """Remove a task."""
    tasks = load_tasks()
    if 0 < task_id <= len(tasks):
        removed = tasks.pop(task_id - 1)
        save_tasks(tasks)
        click.echo(f"🗑 Removed task: {removed['task']}")
    else:
        click.echo("⚠ Invalid task ID.")

if __name__ == "__main__":
    cli()
