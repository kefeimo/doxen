"""Discovery orchestrator - runs all Phase 1 analysis agents."""

from pathlib import Path
from typing import Any, Dict, Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from doxen.agents.repository_analyzer import RepositoryAnalyzer
from doxen.agents.workflow_mapper import WorkflowMapper
from doxen.agents.discovery_reporter import DiscoveryReporter
from doxen.analyzer.llm_analyzer import LLMAnalyzer

console = Console()


class DiscoveryOrchestrator:
    """Orchestrate Phase 1 discovery analysis."""

    def __init__(
        self,
        repo_path: Path,
        output_dir: Path,
        llm_analyzer: Optional[LLMAnalyzer] = None,
    ):
        """Initialize discovery orchestrator.

        Args:
            repo_path: Path to repository to analyze
            output_dir: Directory to save analysis outputs
            llm_analyzer: Optional LLM analyzer for semantic understanding
        """
        self.repo_path = repo_path
        self.output_dir = output_dir
        self.llm = llm_analyzer

        # Initialize agents
        self.repo_analyzer = RepositoryAnalyzer(llm_analyzer=llm_analyzer)
        self.workflow_mapper = WorkflowMapper(llm_analyzer=llm_analyzer)
        # self.arch_extractor = ArchitectureExtractor(llm_analyzer=llm_analyzer)  # TODO

        # Initialize reporter
        self.reporter = DiscoveryReporter(output_dir)

        # Storage for analysis results
        self.results: Dict[str, Any] = {}

    def run_discovery(self) -> Dict[str, Any]:
        """Run complete Phase 1 discovery analysis.

        Returns:
            Combined analysis results
        """
        console.print("\n[bold cyan]Phase 1: Discovery & Analysis[/bold cyan]")
        console.print(f"Repository: [cyan]{self.repo_path}[/cyan]")
        console.print(f"Output: [cyan]{self.output_dir}[/cyan]\n")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Step 1: Repository Analysis
            task1 = progress.add_task("Analyzing repository structure...", total=None)
            repo_analysis = self.repo_analyzer.analyze(self.repo_path)
            self.results["repository"] = repo_analysis
            progress.remove_task(task1)
            console.print("✓ Repository analysis complete")

            # Step 2: Workflow Mapping
            task2 = progress.add_task("Mapping workflows and APIs...", total=None)
            workflow_analysis = self.workflow_mapper.analyze(
                self.repo_path, repo_analysis
            )
            self.results["workflows"] = workflow_analysis
            progress.remove_task(task2)
            console.print("✓ Workflow analysis complete")

            # Step 3: Architecture Extraction (TODO)
            # task3 = progress.add_task("Extracting architecture...", total=None)
            # arch_analysis = self.arch_extractor.analyze(
            #     self.repo_path, repo_analysis, workflow_analysis
            # )
            # self.results["architecture"] = arch_analysis
            # progress.remove_task(task3)
            # console.print("✓ Architecture analysis complete")

        # Save reports
        console.print("\n[bold cyan]Saving analysis reports...[/bold cyan]")
        self._save_reports()

        # Print summary
        self._print_summary()

        return self.results

    def _save_reports(self) -> None:
        """Save analysis reports to disk."""
        # Save repository analysis
        if "repository" in self.results:
            report_path = self.reporter.save_repository_analysis(
                self.results["repository"]
            )
            console.print(f"  → {report_path.name}")

        # Save workflow analysis
        if "workflows" in self.results:
            report_path = self.reporter.save_workflow_analysis(
                self.results["workflows"]
            )
            console.print(f"  → {report_path.name}")

        # Save architecture analysis (TODO)
        # if "architecture" in self.results:
        #     report_path = self.reporter.save_architecture_analysis(
        #         self.results["architecture"]
        #     )
        #     console.print(f"  → {report_path.name}")

        # Save combined JSON
        summary_path = self.reporter.save_discovery_summary(self.results)
        console.print(f"  → {summary_path.name}")

    def _print_summary(self) -> None:
        """Print summary of discovery results."""
        console.print("\n[bold green]Discovery Summary:[/bold green]\n")

        # Repository stats
        if "repository" in self.results:
            repo = self.results["repository"]
            console.print(f"[bold]Repository:[/bold] {repo['repo_name']}")

            languages = repo.get("languages", {})
            if languages:
                lang_list = ", ".join(
                    f"{lang} ({count})" for lang, count in list(languages.items())[:3]
                )
                console.print(f"[bold]Languages:[/bold] {lang_list}")

            entry_points = repo.get("entry_points", [])
            console.print(f"[bold]Entry Points:[/bold] {len(entry_points)}")

            components = repo.get("components", [])
            console.print(f"[bold]Components:[/bold] {len(components)}")

        # Workflow stats
        if "workflows" in self.results:
            workflows = self.results["workflows"]

            endpoints = workflows.get("api_endpoints", [])
            console.print(f"[bold]API Endpoints:[/bold] {len(endpoints)}")

            integrations = workflows.get("integrations", [])
            console.print(f"[bold]Integrations:[/bold] {len(integrations)}")

            user_flows = workflows.get("user_flows", [])
            console.print(f"[bold]User Flows:[/bold] {len(user_flows)}")

        console.print(f"\n[bold cyan]→ Analysis saved to:[/bold cyan] {self.output_dir}")
        console.print()
