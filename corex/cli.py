"""
CoreX CLI - Main entry point for all commands
"""

import os
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .commands.command_registry import register_commands
from .utils import get_project_root

console = Console()


@click.group()
@click.version_option(version="1.0.0", prog_name="CoreX")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.pass_context
def main(ctx: click.Context, verbose: bool) -> None:
    """
    CoreX - A comprehensive Django scaffolding framework
    
    Create production-ready Django apps with a single command.
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    
    if verbose:
        console.print("[bold blue]CoreX[/bold blue] - Django Scaffolding Framework")


# Register all commands
register_commands(main)


if __name__ == "__main__":
    main()