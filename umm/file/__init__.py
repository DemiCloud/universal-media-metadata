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

from umm.schema import normalize
from umm.schema import validate as validate_schema
from umm._vars import Constants

# endregion

cmd = typer.Typer()

# region filetypes
def _get_filetypes() -> dict:
    mapping_file = importlib.resources.files("umm") / "assets" / Constants.Files.MAPPING
    with open(mapping_file, "r", encoding="utf-8") as file:
        mapping_dict = json.load(file)
    return mapping_dict

mappings = _get_filetypes()
filetypes = Enum("filetype", tuple(mappings.keys()))
possible_filetypes = [x.name for x in filetypes]
# endregion


def _version_map(file_type: str, file_version: version.Version) -> str:
    return mappings[file_type]["versions"][str(file_version)]


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
    input_file: Annotated[Path, typer.Option("--file", "-f")],
) -> None:
    """Validates a UMM file

    Args:
      input_file: UMM file to validate
    """
    umm = get_umm(input_file)
    if validate_schema(umm):
        print(f"{input_file} is a valid UMM version {umm['info']['version']} file")
    else:
        print(f"{input_file} is not a valid UMM file")


@cmd.command()
def convert(
    input_file: Annotated[Path, typer.Option("--file", "-f")],
    output_file: Annotated[Path, typer.Option("--output", "-o")],
    file_type: Annotated[filetypes, typer.Option("--type", "-t")] = None,
) -> None:
    """Convert UMM to other filetypes"""
    output_file = pathlib.Path(output_file).resolve()
    umm = get_umm(input_file)
    umm_version = umm["info"]["version"]

    if file_type is None:
        if not (file_type := output_file.suffix[1:]):
            print("Could not determine file type.")
            print("Try explicitly specifying the file type with the -o flag.")
            return
        if file_type not in possible_filetypes:
            print(f"File type {file_type} not supported")
            print(
                "If you're sure this file type is supported, "
                "specify it with the -o flag."
            )
            return
    else:
        file_type = file_type.name

    match file_type:
        case "id3":
            # not yet implemented
            pass
        case "test":
            pass
        case _:
            template_version = _version_map(file_type, umm_version)
            template_file = (
                importlib.resources.files("umm")
                / "assets"
                / "templates"
                / file_type
                / f"{template_version}.template"
            )
            with open(template_file, mode="r", encoding="utf-8") as file:
                template = Template(file.read())
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(template.render(umm=umm))

            print(f"Successfully converted {input_file} to {output_file}.")


@cmd.command()
def generate():
    """Generates a new UMM"""
    print("Hello World")
