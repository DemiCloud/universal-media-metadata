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
import typing
import jinja2

import typer
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


def _get_type(filetype: str) -> str:
    mapping_dict = _get_mappings()
    return mapping_dict[filetype]["type"]


mappings = _get_mappings()
filetypes = Enum("filetype", {k: k for k in mappings})
possible_filetypes = [x.name for x in filetypes]
# endregion


def _version_map(file_type: str, umm_version: version.Version) -> str:
    umm_versions_map = list(mappings[file_type]["versions"].items())
    for i in umm_versions_map:
        if umm_version >= version.parse(i[1]):
            minimum_version = i
        else:
            break
    return minimum_version[0]


def _get_template(template_file: pathlib.Path) -> jinja2.environment.Template:
    env = jinja2.Environment(
        loader=jinja2.PackageLoader(
            "umm",
            package_path="assets/templates",
            encoding="utf-8",
        ),
        auto_reload=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    return env.get_template(str(template_file))


def _render_template():
    pass


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
    input_file: Annotated[pathlib.Path, typer.Option("--file", "-f")],
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
    input_file: Annotated[pathlib.Path, typer.Option("--file", "-f")] = "-",
    output_file: Annotated[pathlib.Path, typer.Option("--output", "-o")] = "-",
    output_type: Annotated[filetypes, typer.Option("--type", "-t")] = None,
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

    if output_type is None:
        extensions = _get_extensions()
        for key, value in extensions.items():
            if output_file.suffix[1:] in value:
                output_type = key
                break
        if output_type is None:
            print("Could not determine file type.")
            print("Try explicitly specifying the file type with the -o flag.")
            raise typer.Exit(1)
    else:
        output_type = output_type.name

    map_type = _get_type(output_type)
    match map_type:
        case "id3":
            # not yet implemented
            pass
        case "template":
            template_version = _version_map(output_type, umm_version)
            template_file = (
                pathlib.Path(output_type)
                / f"{template_version}.{Constants.Template.EXTENSION}"
            )
            template = _get_template(template_file)
            if str(output_file) == "-":
                sys.stdout.write(template.render(umm=umm))
            else:
                with open(output_file, "w", encoding="utf-8") as file:
                    file.write(template.render(umm=umm))
        case _:
            print(f"{map_type} is not recognized")
            raise typer.Exit(1)


@cmd.command()
def generate():
    """Generates a new UMM"""
    print("Hello World")
