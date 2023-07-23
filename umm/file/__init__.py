# file
"""Manage metadata files
"""

# region imports
import datetime
import json
import os
import sys
import tomllib
from pathlib import Path

import jsonschema
import typer
from packaging import version
# This overwrites `print` on purpose
from rich import print  # pylint: disable=redefined-builtin
from rich.pretty import pprint
from typing_extensions import Annotated

import umm.schema as Schema
# endregion

SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(sys.argv[0])))
SCHEMA_DIR = Path(SCRIPT_DIR,"schemas")

cmd = typer.Typer()


def construct_opf():
  """Construct OPF File
  """

@cmd.command()
def convert(
  input_file: Annotated[
    Path,
    typer.Option(
      "--file",
      "-f"
    )
  ],
  file_type: Annotated[
    str,
    typer.Option(
      "--type",
      "-t"
    )
  ],
  output_file: Annotated[
    str,
    typer.Option(
      "--output",
      "-o"
    )
  ]
) -> None:
  """Convert UMM to other filetypes
  """
  input_file = os.path.abspath(os.path.expanduser(input_file))
  match file_type.lower():
    case "test":
      with open(input_file,"rb") as file:
        # print(file.read())
        # umm=tomlkit.parse(file.read()).unwrap()
        umm = tomllib.load(file)
      umm = Schema.normalize(umm,os.path.dirname(input_file))
      Schema.validate(umm)
    case "opf":
      print(f"XML here: {output_file}")

@cmd.command()
def generate():
  """Generates a new UMM
  """
  print("Hello World")
