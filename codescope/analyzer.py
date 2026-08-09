import ast
import json
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()


def analyze_project(path, export=None):
    project_path = Path(path)

    total_files = 0
    total_dirs = 0
    total_lines = 0
    todo_count = 0
    function_count = 0
    class_count = 0
    import_count = 0
    if_count = 0
    for_count = 0
    while_count = 0

    extensions = {}
    largest_files = []
    languages = set()

    ignored_dirs = {
    "venv",
    ".venv",
    "__pycache__",
    ".git",
    ".pytest_cache",
    "node_modules",
    }   

    language_map = {
        ".py": "Python",
        ".md": "Markdown",
        ".toml": "TOML",
        ".js": "JavaScript",
        ".java": "Java",
        ".cpp": "C++",
        ".c": "C",
        ".h": "C/C++ Header",
        ".hpp": "C++ Header",
        ".html": "HTML",
        ".css": "CSS",
    }

    text_extensions = {
        ".py",
        ".md",
        ".txt",
        ".toml",
        ".json",
        ".csv",
        ".js",
        ".java",
        ".cpp",
        ".c",
        ".h",
        ".hpp",
        ".html",
        ".css",
    }

    for item in project_path.rglob("*"):

        if any(
            part in ignored_dirs or part.endswith(".egg-info")
            for part in item.parts
        ):
            continue

        if item.is_dir():
            total_dirs += 1

        elif item.is_file():
            total_files += 1

            ext = item.suffix.lower()

            if not ext.strip():
                ext = "[no extension]"

            extensions[ext] = extensions.get(ext, 0) + 1

            language = language_map.get(ext)

            if language:
                languages.add(language)

            size = item.stat().st_size
            largest_files.append((size, str(item)))

            if ext in text_extensions:
                try:
                    with open(item, "r", encoding="utf-8") as f:
                        lines = f.readlines()

                    total_lines += len(lines)

                    if ext == ".py":
                        try:
                            tree = ast.parse("".join(lines))

                            for node in ast.walk(tree):

                                if isinstance(
                                    node,
                                    (ast.FunctionDef, ast.AsyncFunctionDef),
                                ):
                                    function_count += 1

                                elif isinstance(node, ast.ClassDef):
                                    class_count += 1

                                elif isinstance(
                                    node,
                                    (ast.Import, ast.ImportFrom),
                                ):
                                    import_count += 1

                                elif isinstance(node, ast.If):
                                    if_count += 1

                                elif isinstance(node, ast.For):
                                    for_count += 1

                                elif isinstance(node, ast.While):
                                    while_count += 1

                        except SyntaxError as error:
                            console.print(
                                f"[bold red]Could not parse Python file "
                                f"{item}: {error}[/bold red]"
                            )

                    for line in lines:
                        if "TODO" in line or "FIXME" in line:
                            todo_count += 1

                except Exception as error:
                    console.print(
                        f"[bold red]Could not read {item}: {error}[/bold red]"
                    )

    largest_files.sort(reverse=True)

    results = {
        "total_files": total_files,
        "total_directories": total_dirs,
        "total_lines": total_lines,
        "todo_count": todo_count,
        "languages": list(languages),
        "python_stats": {
        "functions": function_count,
        "classes": class_count,
        "imports": import_count,
        "if_statements": if_count,
        "for_loops": for_count,
        "while_loops": while_count,
        },
        "extensions": extensions,
    }

    if export:
        with open(export, "w") as f:
            json.dump(results, f, indent=4)

        console.print(
            f"[bold green]Exported report to {export}[/bold green]"
        )

    table = Table(title="CodeScope Analysis")

    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Total Files", str(total_files))
    table.add_row("Total Directories", str(total_dirs))
    table.add_row("Total Lines", str(total_lines))
    table.add_row("TODO/FIXME Count", str(todo_count))

    console.print(table)

    ext_table = Table(title="File Types")

    ext_table.add_column("Extension", style="magenta")
    ext_table.add_column("Count", style="yellow")

    for ext, count in sorted(extensions.items()):
        ext_table.add_row(ext, str(count))

    console.print(ext_table)

    largest_table = Table(title="Largest Files")

    largest_table.add_column("Size (bytes)", style="red")
    largest_table.add_column("File", style="blue")

    for size, file in largest_files[:10]:
        largest_table.add_row(str(size), file)

    console.print(largest_table)

    console.print("\n[bold cyan]Languages Detected[/bold cyan]")

    for lang in sorted(languages):
        console.print(f"- {lang}")

    console.print("\n[bold cyan]Python Stats[/bold cyan]")

    console.print(f"- Functions: {function_count}")
    console.print(f"- Classes: {class_count}")
    console.print(f"- Imports: {import_count}")
    console.print(f"- If Statements: {if_count}")
    console.print(f"- For Loops: {for_count}")
    console.print(f"- While Loops: {while_count}")
    return results