# file
"""Manage metadata files
"""

# region imports
import importlib
import tomllib
import pathlib
import json
import sys

from enum import Enum
from pathlib import Path
import typing

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
def _get_mappings() -> dict:
    mapping_file = importlib.resources.files("umm") / "assets" / Constants.Files.MAPPING
    with open(mapping_file, "r", encoding="utf-8") as file:
        mapping_dict = json.load(file)
    return mapping_dict


def _get_extensions() -> dict:
    mapping_dict = _get_mappings()
    return {
        key: val["extension"] for key, val in mapping_dict.items() if "extension" in val
    }


mappings = _get_mappings()
filetypes = Enum("filetype", {k: k for k in mappings})
possible_filetypes = [x.name for x in filetypes]
# endregion


def _version_map(file_type: str, file_version: version.Version) -> str:
    return mappings[file_type]["versions"][str(file_version)]


def get_umm(input_file: typing.BinaryIO | typing.TextIO) -> dict:
    """Opens and parses the UMM file

    Args:
      input_file (str): Path to the UMM file

    Returns:
      _type_: returns the UMM file as a dict
    """
    # input_file = pathlib.Path(input_file).resolve()
    # with input_file.open("rb") as file:
    #     umm = tomllib.load(file)
    umm = tomllib.loads(input_file.read())
    umm = normalize(umm)
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
    input_file: Annotated[Path, typer.Option("--file", "-f")] = "-",
    output_file: Annotated[Path, typer.Option("--output", "-o")] = "-",
    file_type: Annotated[filetypes, typer.Option("--type", "-t")] = None,
) -> None:
    """Convert UMM to other filetypes"""
    if str(input_file) == "-":
        input_file = sys.stdin
    else:
        input_file = pathlib.Path(input_file).resolve()
        input_file = open(input_file, "r", encoding="utf-8")
    if str(output_file) != "-":
        output_file = pathlib.Path(output_file).resolve()

    umm = get_umm(input_file)
    umm_version = umm["info"]["version"]

    if file_type is None:
        extensions = _get_extensions()
        for key, value in extensions.items():
            if output_file.suffix[1:] in value:
                file_type = key
                break
        if file_type is None:
            print("Could not determine file type.")
            print("Try explicitly specifying the file type with the -o flag.")
            raise typer.Exit(1)
    else:
        file_type = file_type.name

    match file_type:
        case "id3":
            # not yet implemented
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

            if str(output_file) == "-":
                sys.stdout.write(template.render(umm=umm))
            else:
                with open(output_file, "w", encoding="utf-8") as file:
                    file.write(template.render(umm=umm))


@cmd.command()
def generate():
    """Generates a new UMM"""
    print("Hello World")
