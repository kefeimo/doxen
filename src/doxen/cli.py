"""Command-line interface for Doxen."""

import os
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from doxen import __version__
from doxen.extractor.python import PythonExtractor
from doxen.analyzer.llm_analyzer import LLMAnalyzer
from doxen.generator.markdown import MarkdownGenerator
from doxen.utils.git import GitAnalyzer
from doxen.utils.metadata import MetadataBuilder

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
        # Initialize components
        git_analyzer = GitAnalyzer(repo_path)
        metadata_builder = MetadataBuilder()
        markdown_gen = MarkdownGenerator(output)

        # Check for LLM configuration (Bedrock or direct API)
        use_bedrock = os.environ.get("CLAUDE_CODE_USE_BEDROCK") == "1"
        api_key = os.environ.get("ANTHROPIC_API_KEY")

        if use_bedrock:
            # AWS Bedrock
            aws_profile = os.environ.get("AWS_PROFILE")
            if not aws_profile:
                console.print("[yellow]⚠ AWS_PROFILE not set - running without LLM analysis[/yellow]")
                use_llm = False
            else:
                console.print(f"[dim]Using AWS Bedrock (profile: {aws_profile})[/dim]")
                llm_analyzer = LLMAnalyzer(use_bedrock=True)
                use_llm = True
        elif api_key:
            # Direct Anthropic API
            console.print("[dim]Using Anthropic API[/dim]")
            llm_analyzer = LLMAnalyzer(api_key)
            use_llm = True
        else:
            console.print("[yellow]⚠ No LLM configuration found - running without LLM analysis[/yellow]")
            console.print("[dim]Set ANTHROPIC_API_KEY or CLAUDE_CODE_USE_BEDROCK=1[/dim]")
            use_llm = False

        # Scan for Python files
        python_files = list(repo_path.rglob("*.py"))

        if not python_files:
            console.print("[yellow]No Python files found in repository[/yellow]")
            return

        console.print(f"Found {len(python_files)} Python files")

        # Process files
        extractor = PythonExtractor()
        processed = 0

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Analyzing files...", total=len(python_files))

            for py_file in python_files:
                if verbose:
                    console.print(f"[dim]Processing: {py_file.relative_to(repo_path)}[/dim]")

                # 1. Extract structure with AST
                structure = extractor.extract(py_file)

                if "error" in structure:
                    console.print(f"[yellow]Skipping {py_file.name}: {structure['error']}[/yellow]")
                    progress.advance(task)
                    continue

                # 2. Get git history
                git_history = git_analyzer.get_file_history(py_file)

                # 3. Analyze intent with LLM (if available)
                if use_llm:
                    with open(py_file, "r", encoding="utf-8") as f:
                        code = f.read()
                    llm_analysis = llm_analyzer.analyze_code(code, structure)
                else:
                    llm_analysis = {
                        "purpose": "Analysis not available (no API key)",
                        "relationships": [],
                        "complexity": "unknown",
                        "audience": ["junior", "senior"],
                    }

                # 4. Build metadata
                metadata = metadata_builder.build(structure, llm_analysis, git_history)

                # 5. Generate markdown documentation
                analysis = {
                    **structure,
                    **llm_analysis,
                    "metadata": metadata,
                    "git_history": git_history,
                }

                doc_path = markdown_gen.generate(analysis)
                processed += 1

                progress.advance(task)

        console.print(f"\n[bold green]✓ Analysis complete![/bold green]")
        console.print(f"Processed {processed} files")
        console.print(f"Documentation saved to: [cyan]{output}[/cyan]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        if verbose:
            import traceback
            console.print(traceback.format_exc())
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
