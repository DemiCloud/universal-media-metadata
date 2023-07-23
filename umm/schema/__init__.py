"""Universal Media Metadata Schema"""

# region imports
import datetime
import json
import os
from pathlib import Path

from jsonschema import Draft202012Validator, validators
from jsonschema.exceptions import ValidationError
from packaging import version

# endregion

umm_checker= Draft202012Validator.TYPE_CHECKER.redefine_many(
  {
    "version": lambda _, instance: isinstance(instance, version.Version),
    "path": lambda _, instance: isinstance(instance, Path),
    "date": lambda _, instance: isinstance(instance, datetime.date),
  }
)

UmmValidator = validators.extend(Draft202012Validator, type_checker=umm_checker)

def validate(
  umm: dict,
) -> None:
  """Validate UMM
  """
  umm_version = umm['info']['version']
  schema_file = Path(
    os.path.join(
      "./umm/assets/schemas/",
      umm['info']['class'],
      f"{str(umm_version)}.schema"
    )
  )
  with open(schema_file,"rb") as file:
    schema = json.load(file)
  validator = UmmValidator(schema)
  validator.validate(umm)
  print("validation successful")

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
