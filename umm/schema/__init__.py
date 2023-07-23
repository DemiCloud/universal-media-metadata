"""Universal Media Metadata Schema"""

# region imports
import datetime
import json
import os
from pathlib import Path

from jsonschema import Draft4Validator, FormatChecker, validators
from jsonschema.exceptions import ValidationError
from packaging import version
# endregion

# region Custom Validators
all_validators = dict(Draft4Validator.VALIDATORS)

def is_version(validator, value, instance, schema) -> None:
  """Custom jsonscheme validation method for Version"""
  # pylint: disable=unused-argument
  if not isinstance(instance,version.Version):
    yield ValidationError(f"{instance} is not a valid version number")
all_validators['is_version'] = is_version

def is_path(validator, value, instance, schema) -> None:
  """Custom jsonscheme validation method for pathlib Paths"""
  # pylint: disable=unused-argument
  if not isinstance(instance,Path):
    yield ValidationError(f"{instance} is not a valid path")
all_validators['is_path'] = is_path
# endregion



def normalize(
  umm: dict,
  umm_path: Path
) -> dict:
  """normalized the metadata dictionary

  Args:
      umm (dict): metadata dictionary

  Returns:
      dict: normalized metadata dictionary
  """
  try:
    umm['info']['version'] = version.parse(umm['info']['version'])
  except version.InvalidVersion:
    print(f"{umm['info']['version']} is not a valid version number")

  if not isinstance(umm['metadata']['date'],datetime.date):
    print(f"{umm['metadata']['date']} is not a valid date format. Date should be YYYY-MM-DD")

  if os.path.isabs(os.path.abspath(os.path.expanduser(umm['metadata']['cover']))):
    umm['metadata']['cover'] = os.path.abspath(os.path.expanduser(umm['metadata']['cover']))
  else:
    umm['metadata']['cover']= os.path.join(umm_path,umm['metadata']['cover'])


  try:
    umm['metadata']['cover'] = Path(umm['metadata']['cover'])
  except TypeError:
    print("metadata.cover should be a valid path")
  return umm

def schema_validate(
  umm: dict,
) -> None:
  """Validate UMM
  """
  pass
  # umm_version = umm['info']['version']
  # schema_file = Path(os.path.join(SCHEMA_DIR),f"{str(umm_version)}.schema")
  # with open(schema_file,"rb") as file:
  #   schema = json.load(file)
  # validate(umm,schema=schema)
