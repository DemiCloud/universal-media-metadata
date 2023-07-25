"""
Module Docstring
"""

__author__ = "DemiCloud"
__version__ = "0.1.0"
__license__ = "MIT"

# region imports
import inspect
import os
from pathlib import Path

import typer
from rich.console import Console

from umm._vars import Constants
from umm._vars import Variable
from umm.file import cmd

# endregion

# region Typer Definitions
app = typer.Typer(rich_markup_mode="rich", no_args_is_help=True)
app.add_typer(cmd, name="file")
console = Console()
# endregion


@app.command("version")
def app_version() -> None:
    """Print version and exit"""
    print(f"{Constants.NAME}: Version {__version__}")


@app.callback()
def main() -> None:
    """CLI tool to manage Netbox"""
    Variable.proj_dir = Path(__file__).parent.resolve()


def cli(app_name: str = "umm-cli"):
    """Entry Point for the CLI Application"""
    Variable.app_name = app_name
    Variable.rel_dir = Path(inspect.stack()[1].filename).parent.resolve()
    app()
