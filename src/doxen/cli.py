"""Command-line interface for Doxen."""

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console

from doxen import __version__

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="doxen")
def main() -> None:
    """Doxen - Knowledge layer for code.

    Transform codebases into structured, testable, and AI-ready documentation.
    """
    pass


@main.command()
@click.argument("repo_path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    default=".doxen/docs",
    help="Output directory for generated documentation",
)
@click.option(
    "--languages",
    "-l",
    multiple=True,
    default=["python", "javascript"],
    help="Languages to analyze (default: python, javascript)",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose output",
)
def analyze(
    repo_path: Path,
    output: Path,
    languages: tuple[str, ...],
    verbose: bool,
) -> None:
    """Analyze a codebase and generate documentation.

    REPO_PATH: Path to the repository to analyze
    """
    console.print(f"[bold green]Doxen v{__version__}[/bold green]")
    console.print(f"Analyzing repository: [cyan]{repo_path}[/cyan]")
    console.print(f"Output directory: [cyan]{output}[/cyan]")
    console.print(f"Languages: [cyan]{', '.join(languages)}[/cyan]")

    if verbose:
        console.print("[dim]Verbose mode enabled[/dim]")

    # Create output directory
    output.mkdir(parents=True, exist_ok=True)

    try:
        # TODO: Implement the analysis pipeline
        # 1. Scan repository for files
        # 2. Extract structure with AST
        # 3. Analyze intent with LLM
        # 4. Generate markdown documentation
        # 5. Add git history traceability

        console.print("[yellow]⚠ Analysis pipeline not yet implemented[/yellow]")
        console.print("[dim]This is a skeleton CLI - implementation coming next[/dim]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)


@main.command()
@click.argument("repo_path", type=click.Path(exists=True, path_type=Path))
def scan(repo_path: Path) -> None:
    """Scan a repository and show file statistics.

    REPO_PATH: Path to the repository to scan
    """
    console.print(f"Scanning repository: [cyan]{repo_path}[/cyan]")

    # TODO: Implement file scanning
    console.print("[yellow]⚠ Scan not yet implemented[/yellow]")


if __name__ == "__main__":
    main()
