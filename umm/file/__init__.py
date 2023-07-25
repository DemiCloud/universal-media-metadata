# file
"""Manage metadata files
"""

# region imports
import importlib
import tomllib
import pathlib
import json

from enum import Enum
from pathlib import Path

import typer
from jinja2 import Template
from packaging import version

# This overwrites `print` on purpose
from rich import print  # pylint: disable=redefined-builtin
from typing_extensions import Annotated

from ..schema import normalize
from ..schema import validate as validate_schema

# endregion

cmd = typer.Typer()


# region convert templates to an enum
# This section dynamically creates a list of options
# for filetypes to choose for conversion
def _get_filetypes_enum() -> Enum:
  type_dict = {"id3": "id3"}
  templates = [
    resource.name
    for resource in (
      importlib.resources.files("umm") / "assets" / "templates"
    ).iterdir()
    if resource.is_dir()
  ]
  for template in templates:
    type_dict[template] = template
  return Enum("filetype", type_dict)


filetypes = _get_filetypes_enum()
# endregion


@cmd.command()
def test():
  """Test command"""


def _version_map(file_type: str, file_version: version.Version) -> str:
  mapping_file = importlib.resources.files("umm") / "assets" / "mapping.json"
  with open(mapping_file, "rb") as file:
    mappings = json.load(file)
  return mappings[file_type][str(file_version)]


def get_umm(input_file: str):
  """Opens and parses the UMM file

  Args:
    input_file (str): Path to the UMM file

  Returns:
    _type_: returns the UMM file as a dict
  """
  input_file = pathlib.Path(input_file).resolve()
  with input_file.open("rb") as file:
    umm = tomllib.load(file)
  umm = normalize(umm, input_file.parent)
  return umm


@cmd.command()
def validate(
  input_file: Annotated[
    Path,
    typer.Option("--file", "-f")
  ],
) -> None:
  """Validates a UMM file

  Args:
    input_file: UMM file to validate
  """
  umm = get_umm(input_file)
  if validate_schema(umm):
    print(
      f"{input_file} is a valid UMM version {umm['info']['version']} file")
  else:
    print(f"Could not validate {input_file}")


@cmd.command()
def convert(
  input_file: Annotated[Path, typer.Option("--file", "-f")],
  file_type: Annotated[filetypes, typer.Option("--type", "-t")],
  output_file: Annotated[str, typer.Option("--output", "-o")],
) -> None:
  """Convert UMM to other filetypes"""
  output_file = pathlib.Path(output_file).resolve()
  umm = get_umm(input_file)
  umm_version = umm["info"]["version"]
  match file_type.value:
    case "id3":
      # not yet implemented
      pass
    case "test":
      pass
    case _:
      template_version = _version_map(file_type.value, umm_version)
      template_file = (
        importlib.resources.files("umm")
        / "assets"
        / "templates"
        / file_type.value
        / f"{template_version}.template"
      )
      print(_version_map("opf", umm_version))
      with open(template_file, mode="r", encoding="utf-8") as file:
        template = Template(file.read())
      with open(output_file, "w", encoding="utf-8") as file:
        file.write(template.render(umm=umm))


@cmd.command()
def generate():
  """Generates a new UMM"""
  print("Hello World")
