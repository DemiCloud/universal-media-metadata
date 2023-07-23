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

import umm._vars as Vars
import umm.file as File
# endregion

# region Typer Definitions
cmd = typer.Typer(
  rich_markup_mode="rich",
  no_args_is_help=True
)
cmd.add_typer(File.cmd, name="file")
console = Console()
# endregion

@cmd.command("version")
def cmd_version() -> None:
  """Print version and exit
  """
  print(f"{Vars.Constants.NAME}: Version {__version__}")

@cmd.callback()
def main() -> None:
  """ CLI tool to manage Netbox """
  Vars.Variable.proj_dir = Path(os.path.dirname(os.path.realpath(__file__)))

def cli(
  app_name: str = "umm-cli"
):
  """ Entry Point for the CLI Application"""
  Vars.Variable.app_name = app_name
  Vars.Variable.rel_dir = Path(
    os.path.abspath(
      os.path.expanduser(
        os.path.dirname(
          inspect.stack()[1].filename
        )
      )
    )
  )
  cmd()
