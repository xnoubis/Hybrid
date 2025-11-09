#!/usr/bin/env python3
"""
Interactive Dialectical Solution Engine CLI
"""

import sys
from typing import Optional, Dict, Any

try:
    from rich.console import Console
    from rich.prompt import Prompt, Confirm
    from rich.panel import Panel
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    Console = None

from ..dialectical.engine import SolutionEngine, SolutionType


class DialecticalCLI:
    """Interactive CLI for dialectical reasoning"""

    def __init__(self):
        self.engine = SolutionEngine()
        if RICH_AVAILABLE:
            self.console = Console()
        else:
            self.console = None

    def print(self, message: str, style: Optional[str] = None):
        """Print with or without rich"""
        if self.console:
            self.console.print(message, style=style)
        else:
            print(message)

    def prompt(self, message: str, default: str = "") -> str:
        """Prompt with or without rich"""
        if RICH_AVAILABLE:
            return Prompt.ask(message, default=default)
        else:
            response = input(f"{message} [{default}]: " if default else f"{message}: ")
            return response or default

    def confirm(self, message: str) -> bool:
        """Confirm with or without rich"""
        if RICH_AVAILABLE:
            return Confirm.ask(message)
        else:
            response = input(f"{message} (y/n): ")
            return response.lower() in ['y', 'yes']

    def run(self):
        """Run interactive session"""
        self.print("\n[bold blue]Dialectical Solution Engine[/bold blue]", style="bold")
        self.print("=" * 60)
        self.print("\nFind solutions through impossibility crystallization\n")

        # Phase 1: Crystallize Problem
        self.print("[bold]Phase 1: Crystallize the Problem[/bold]", style="bold green")
        surface = self.prompt("What's the surface-level tension?")
        impossibility = self.prompt("What seems impossible?")

        reasons = []
        self.print("\nWhy does it seem impossible? (enter blank to finish)")
        while True:
            reason = self.prompt("Reason")
            if not reason:
                break
            reasons.append(reason)

        problem = self.engine.crystallize_problem(surface, impossibility, reasons)
        self.print(f"\n✓ Problem crystallized: {problem.impossibility}\n", style="green")

        # Phase 2: Map Perspectives
        self.print("[bold]Phase 2: Map Extreme Perspectives[/bold]", style="bold green")

        perspectives_data = {}
        perspective_names = ['A', 'B']

        for name in perspective_names:
            self.print(f"\n[bold]Perspective {name}:[/bold]")
            claim = self.prompt(f"  What does {name} claim?")
            victory = self.prompt(f"  What's {name}'s victory condition?")

            assumptions = []
            self.print(f"  What does {name} assume? (blank to finish)")
            while True:
                assumption = self.prompt("    Assumption")
                if not assumption:
                    break
                assumptions.append(assumption)

            non_negotiables = []
            self.print(f"  What can't {name} compromise on? (blank to finish)")
            while True:
                non_neg = self.prompt("    Non-negotiable")
                if not non_neg:
                    break
                non_negotiables.append(non_neg)

            perspectives_data[name] = {
                'claim': claim,
                'victory': victory,
                'assumptions': assumptions,
                'non_negotiables': non_negotiables
            }

        perspectives = self.engine.map_perspectives(perspectives_data)
        self.print(f"\n✓ Mapped {len(perspectives)} perspectives\n", style="green")

        # Phase 3: Identify Negation
        self.print("[bold]Phase 3: Identify Negation Zone[/bold]", style="bold green")
        negation = self.engine.identify_negation()

        self.print(f"\nContradiction: {negation.contradiction}")
        self.print(f"\nImpossibility Core:\n  {negation.impossibility_core}")
        self.print(f"\nCreative Tension:\n  {negation.creative_tension}")

        self.print("\nBoth True:")
        for truth in negation.both_true:
            self.print(f"  • {truth}")

        self.print("\nNeither Sufficient:")
        for insufficiency in negation.neither_sufficient:
            self.print(f"  • {insufficiency}")

        self.print("\n✓ Negation zone identified\n", style="green")

        # Phase 4: Crystallize Solution
        self.print("[bold]Phase 4: Crystallize Solution[/bold]", style="bold green")

        if self.confirm("Auto-detect solution type?"):
            solution = self.engine.crystallize_solution()
        else:
            self.print("\nSolution types:")
            for i, stype in enumerate(SolutionType, 1):
                self.print(f"  {i}. {stype.value}")

            choice = int(self.prompt("Choose solution type (1-5)", default="1"))
            solution_type = list(SolutionType)[choice - 1]
            solution = self.engine.crystallize_solution(solution_type=solution_type)

        self.print(f"\n[bold]Solution Type:[/bold] {solution.solution_type.value}")
        self.print(f"\n[bold]Description:[/bold]\n{solution.description}")
        self.print(f"\n[bold]How it works:[/bold]\n{solution.how_it_works}")

        self.print(f"\n[bold]Preserves from A:[/bold]")
        for item in solution.preserves_A:
            self.print(f"  • {item}")

        self.print(f"\n[bold]Preserves from B:[/bold]")
        for item in solution.preserves_B:
            self.print(f"  • {item}")

        self.print(f"\n[bold]Transcends:[/bold]\n{solution.transcends}")

        self.print(f"\n[bold]Implementation:[/bold]\n{solution.implementation_sketch}")

        self.print(f"\n[bold]New Questions:[/bold]")
        for question in solution.new_questions:
            self.print(f"  • {question}")

        self.print("\n✓ Solution crystallized\n", style="green")

        # Phase 5: Validate
        self.print("[bold]Phase 5: Validate Solution[/bold]", style="bold green")
        validation = self.engine.validate_solution()

        if self.console:
            table = Table(title="Validation Results")
            table.add_column("Criterion", style="cyan")
            table.add_column("Status", style="magenta")
            table.add_column("Message", style="white")

            for criterion, result in validation.items():
                if criterion == 'overall':
                    continue
                status = "✓" if result['passed'] else "✗"
                table.add_row(criterion, status, result['message'])

            self.console.print(table)
        else:
            self.print("\nValidation Results:")
            for criterion, result in validation.items():
                if criterion == 'overall':
                    continue
                status = "✓" if result['passed'] else "✗"
                self.print(f"  {status} {criterion}: {result['message']}")

        overall = validation['overall']
        status = "PASSED" if overall['passed'] else "FAILED"
        self.print(f"\n[bold]Overall: {status}[/bold]", style="green" if overall['passed'] else "red")
        self.print(f"Criteria met: {overall['criteria_met']}/{overall['total_criteria']}\n")

        # Export
        if self.confirm("Export session to JSON?"):
            filename = self.prompt("Filename", default="session.json")
            with open(filename, 'w') as f:
                f.write(self.engine.to_json())
            self.print(f"✓ Exported to {filename}", style="green")

        self.print("\n[bold blue]Session complete![/bold blue]", style="bold")


def main():
    """Entry point"""
    cli = DialecticalCLI()
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\n\nSession interrupted.")
        sys.exit(0)


if __name__ == '__main__':
    main()
